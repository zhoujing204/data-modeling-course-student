"""Submit generated experiment PDF reports to the LabDrop FastAPI server."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import requests

try:
    from .server_health import DEFAULT_CONFIG_PATH, _load_server_url
    from .notebook_info_extractor import is_valid_email, normalize_email
except ImportError:  # Support importing after adding ``util`` to sys.path.
    from server_health import DEFAULT_CONFIG_PATH, _load_server_url
    from notebook_info_extractor import is_valid_email, normalize_email


EXPERIMENTS = {
    1: ("exp-01", "实验一"),
    2: ("exp-02", "实验二"),
    3: ("exp-03", "实验三"),
    4: ("exp-04", "实验四"),
    5: ("exp-05", "实验五"),
    6: ("exp-06", "实验六"),
}


class ReportSubmissionError(RuntimeError):
    """Raised when a report cannot be accepted by the server."""


def _response_payload(response: requests.Response) -> Any:
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return response.text


def _raise_submission_error(response: requests.Response) -> None:
    payload = _response_payload(response)
    message = f"Server returned HTTP {response.status_code}"

    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict):
            code = error.get("code")
            detail = error.get("message")
            request_id = error.get("request_id")
            if code:
                message += f" ({code})"
            if detail:
                message += f": {detail}"
            if request_id:
                message += f" [request_id={request_id}]"
        elif payload:
            message += f": {payload}"
    elif payload:
        message += f": {payload}"

    raise ReportSubmissionError(message)


def submit_pdf_report(
    pdf_path: str | Path,
    student_info: Mapping[str, Any],
    experiment_number: int,
    *,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
    course_run_id: str | None = None,
    timeout: tuple[float, float] = (5.0, 60.0),
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Upload a generated PDF and return its submission receipt.

    ``student_info`` accepts the dictionary returned by
    ``notebook_info_extractor.extract_from_ipynb``. The current course run is
    obtained from the server automatically unless ``course_run_id`` is given.

    Repeating the call with the same PDF and metadata uses the same idempotency
    key, so a network retry will not create an extra submission version.
    """
    if experiment_number not in EXPERIMENTS:
        raise ValueError("experiment_number must be an integer from 1 to 6")

    path = Path(pdf_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"PDF report was not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Report must have a .pdf extension: {path}")

    pdf_data = path.read_bytes()
    if not pdf_data.startswith(b"%PDF-") or b"%%EOF" not in pdf_data:
        raise ValueError(f"Report is not a structurally valid PDF: {path}")

    required_fields = ("class_id", "student_id", "name", "email")
    missing = [field for field in required_fields if not student_info.get(field)]
    if missing:
        raise ValueError(f"Missing student information: {', '.join(missing)}")

    class_id = str(student_info["class_id"]).strip()
    student_id = str(student_info["student_id"]).strip()
    student_name = str(student_info["name"]).strip()
    email = str(student_info["email"]).strip()
    if not is_valid_email(email):
        raise ValueError(
            "Email地址无效，请在Notebook顶部的学生信息表中重新输入有效地址。"
        )
    email = normalize_email(email)
    for field_name, value in {
        "class_id": class_id,
        "student_id": student_id,
        "student_name": student_name,
    }.items():
        if not value or "_" in value or "/" in value or "\\" in value:
            raise ValueError(f"Invalid {field_name} for report submission: {value!r}")

    experiment_id, experiment_name = EXPERIMENTS[experiment_number]
    server_url = _load_server_url(config_path)
    http = session or requests.Session()

    try:
        server_info_response = http.get(
            f"{server_url}/api/v1/server-info",
            headers={"Accept": "application/json"},
            timeout=timeout,
        )
        if not 200 <= server_info_response.status_code < 300:
            _raise_submission_error(server_info_response)
        server_info = _response_payload(server_info_response)
        if not isinstance(server_info, dict):
            raise ReportSubmissionError("Server returned invalid server information")
        if server_info.get("submission_email_supported") is not True:
            raise ReportSubmissionError(
                "LabDrop服务器尚未启用学生邮箱更新功能，请重启或升级服务器后重试。"
            )

        selected_course_run = course_run_id or server_info.get("active_course_run_id")
        if not isinstance(selected_course_run, str) or not selected_course_run:
            raise ReportSubmissionError("Server did not provide an active course run")

        maximum_size = server_info.get("default_max_pdf_bytes")
        if isinstance(maximum_size, int) and len(pdf_data) > maximum_size:
            raise ValueError(
                f"PDF is {len(pdf_data)} bytes; server limit is {maximum_size} bytes"
            )

        upload_filename = (
            f"{class_id}_{student_id}_{student_name}_{experiment_name}.pdf"
        )
        metadata = {
            "course_run_id": selected_course_run,
            "class_id": class_id,
            "student_id": student_id,
            "student_name": student_name,
            "email": email,
            "experiment_id": experiment_id,
        }
        idempotency_material = json.dumps(
            metadata, ensure_ascii=False, sort_keys=True
        ).encode("utf-8") + pdf_data
        idempotency_key = "report-" + hashlib.sha256(idempotency_material).hexdigest()

        response = http.post(
            f"{server_url}/api/v1/submissions",
            data={
                **metadata,
                "client_generated_at": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            },
            files={"report": (upload_filename, pdf_data, "application/pdf")},
            headers={
                "Accept": "application/json",
                "Idempotency-Key": idempotency_key,
            },
            timeout=timeout,
        )
    except requests.RequestException as error:
        raise ReportSubmissionError(
            f"Could not connect to the report server at {server_url}: {error}"
        ) from error

    if not 200 <= response.status_code < 300:
        _raise_submission_error(response)

    receipt = _response_payload(response)
    if not isinstance(receipt, dict) or not receipt.get("submission_id"):
        raise ReportSubmissionError("Server returned an invalid submission receipt")
    if receipt.get("student_email") != email:
        raise ReportSubmissionError(
            "报告已被服务器接收，但学生邮箱未确认更新；请联系教师检查服务器版本。"
        )

    print(
        "报告提交成功: "
        f"{receipt['submission_id']} (version {receipt.get('version', 'unknown')})"
    )
    return receipt
