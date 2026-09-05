import json

from util.report_submission import submit_pdf_report


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
            },
        )

    def post(self, url, **kwargs):
        self.submission = (url, kwargs)
        return FakeResponse(
            201,
            {"submission_id": "submission-1", "version": 1},
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
        {"class_id": "25智能1", "student_id": "B007", "name": "James"},
        1,
        config_path=config_path,
        session=session,
    )

    assert receipt["submission_id"] == "submission-1"
    url, request = session.submission
    assert url == "http://172.20.10.2:8000/api/v1/submissions"
    assert request["data"]["course_run_id"] == "2026-fall"
    assert request["data"]["experiment_id"] == "exp-01"
    assert request["files"]["report"][0] == "25智能1_B007_James_实验一.pdf"
    assert request["headers"]["Idempotency-Key"].startswith("report-")
