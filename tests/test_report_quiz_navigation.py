"""Successful PDF upload triggers browser-side quiz navigation exactly once."""
from unittest.mock import Mock
import json

import pytest
from util import report_submission


@pytest.mark.parametrize('status', [200, 201])
def test_successful_receipt_opens_quiz_without_changing_receipt(tmp_path, monkeypatch, status):
    config = tmp_path/'config.json'
    config.write_text(json.dumps({'server_url': 'https://lab.example.test'}))
    pdf = tmp_path/'report.pdf'
    pdf.write_bytes(b'%PDF-1.4\nsynthetic\n%%EOF')
    info = {'class_id':'class1','student_id':'s1','name':'Student','email':'student@example.test'}
    receipt = {'submission_id':'sub1','version':1,'student_email':info['email'],
               'assessment_available':True,'assessment_url':'/quiz?course_run_id=2027-spring&experiment_id=exp-02'}
    http = Mock()
    http.get.return_value.status_code = 200
    http.get.return_value.json.return_value = {'active_course_run_id':'2027-spring','submission_email_supported':True}
    http.post.return_value.status_code = status
    http.post.return_value.json.return_value = receipt
    navigate = Mock(return_value={'fallback_url':'https://lab.example.test'+receipt['assessment_url']})
    monkeypatch.setattr(report_submission, 'open_assessment_after_upload', navigate)
    # A lightweight display module keeps this unit test independent of a live kernel.
    import sys
    from types import ModuleType
    ipython = ModuleType('IPython')
    display = ModuleType('IPython.display')
    display.HTML = str
    display.display = lambda value: None
    monkeypatch.setitem(sys.modules, 'IPython', ipython)
    monkeypatch.setitem(sys.modules, 'IPython.display', display)
    assert report_submission.submit_pdf_report(pdf, info, 2, config_path=config, session=http) == receipt
    navigate.assert_called_once()
    assert navigate.call_args.kwargs['remote_kernel'] is True


def test_navigation_failure_preserves_accepted_pdf(tmp_path, monkeypatch):
    # Reuse the success path with a display failure; it must not report upload failure.
    config = tmp_path/'config.json'
    config.write_text(json.dumps({'server_url':'https://lab.example.test'}))
    pdf=tmp_path/'report.pdf';pdf.write_bytes(b'%PDF-1.4\n%%EOF')
    http=Mock()
    http.get.return_value.status_code=200
    http.get.return_value.json.return_value={'active_course_run_id':'2027-spring','submission_email_supported':True}
    receipt={'submission_id':'sub1','student_email':'s@example.test','assessment_url':'/quiz?course_run_id=2027-spring&experiment_id=exp-02'}
    http.post.return_value.status_code=201;http.post.return_value.json.return_value=receipt
    monkeypatch.setattr(report_submission,'open_assessment_after_upload',Mock(side_effect=RuntimeError('display unavailable')))
    assert report_submission.submit_pdf_report(pdf,{'class_id':'c','student_id':'s','name':'S','email':'s@example.test'},2,config_path=config,session=http)==receipt
