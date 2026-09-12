import json

import pytest

from util.report_submission import ReportSubmissionError, submit_pdf_report


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload, ensure_ascii=False)

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self):
        self.submission = None

    def get(self, url, **kwargs):
        assert url == "http://172.20.10.2:8000/api/v1/server-info"
        return FakeResponse(
            200,
            {
                "active_course_run_id": "2026-fall",
                "default_max_pdf_bytes": 10 * 1024 * 1024,
                "submission_email_supported": True,
            },
        )

    def post(self, url, **kwargs):
        self.submission = (url, kwargs)
        return FakeResponse(
            201,
            {
                "submission_id": "submission-1",
                "version": 1,
                "student_email": self.submission[1]["data"]["email"],
            },
        )


class LegacyFakeSession(FakeSession):
    def get(self, url, **kwargs):
        assert url == "http://172.20.10.2:8000/api/v1/server-info"
        return FakeResponse(
            200,
            {
                "active_course_run_id": "2026-fall",
                "default_max_pdf_bytes": 10 * 1024 * 1024,
            },
        )


class MismatchedEmailSession(FakeSession):
    def post(self, url, **kwargs):
        self.submission = (url, kwargs)
        return FakeResponse(
            201,
            {
                "submission_id": "submission-1",
                "version": 1,
                "student_email": "wrong@example.com",
            },
        )

def test_submit_pdf_report_builds_server_request(tmp_path):
    config_path = tmp_path / "client_config.json"
    config_path.write_text(
        json.dumps({"server_url": "http://172.20.10.2:8000"}),
        encoding="utf-8",
    )
    pdf_path = tmp_path / "locally-generated-name.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%%EOF\n")
    session = FakeSession()

    receipt = submit_pdf_report(
        pdf_path,
        {
            "class_id": "25智能1",
            "student_id": "B007",
            "name": "James",
            "email": "james@example.com",
        },
        1,
        config_path=config_path,
        session=session,
    )

    assert receipt["submission_id"] == "submission-1"
    url, request = session.submission
    assert url == "http://172.20.10.2:8000/api/v1/submissions"
    assert request["data"]["course_run_id"] == "2026-fall"
    assert request["data"]["experiment_id"] == "exp-01"
    assert request["data"]["email"] == "james@example.com"
    assert request["files"]["report"][0] == "25智能1_B007_James_实验一.pdf"
    assert request["headers"]["Idempotency-Key"].startswith("report-")


def test_submit_pdf_report_rejects_invalid_email_before_request(tmp_path):
    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%%EOF\n")
    session = FakeSession()

    with pytest.raises(ValueError, match="Email地址无效"):
        submit_pdf_report(
            pdf_path,
            {
                "class_id": "25智能1",
                "student_id": "B007",
                "name": "James",
                "email": "未填写",
            },
            1,
            session=session,
        )

    assert session.submission is None


def test_submit_pdf_report_rejects_server_without_email_support(tmp_path):
    config_path = tmp_path / "client_config.json"
    config_path.write_text(
        json.dumps({"server_url": "http://172.20.10.2:8000"}),
        encoding="utf-8",
    )
    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%%EOF\n")
    session = LegacyFakeSession()

    with pytest.raises(ReportSubmissionError, match="尚未启用学生邮箱更新功能"):
        submit_pdf_report(
            pdf_path,
            {
                "class_id": "25智能1",
                "student_id": "B007",
                "name": "James",
                "email": "james@example.com",
            },
            1,
            config_path=config_path,
            session=session,
        )

    assert session.submission is None


def test_submit_pdf_report_requires_email_confirmation_in_receipt(tmp_path):
    config_path = tmp_path / "client_config.json"
    config_path.write_text(
        json.dumps({"server_url": "http://172.20.10.2:8000"}),
        encoding="utf-8",
    )
    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%%EOF\n")

    with pytest.raises(ReportSubmissionError, match="邮箱未确认更新"):
        submit_pdf_report(
            pdf_path,
            {
                "class_id": "25智能1",
                "student_id": "B007",
                "name": "James",
                "email": "james@example.com",
            },
            1,
            config_path=config_path,
            session=MismatchedEmailSession(),
        )
