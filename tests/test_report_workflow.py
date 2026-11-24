"""Execute each real merged notebook cell with local generation/upload doubles."""
import importlib
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('experiment', range(1, 7))
@pytest.mark.parametrize('outcome', ['success', 'generation_failure', 'submission_failure'])
def test_merged_cell_waits_for_generation_and_reports_results(tmp_path, monkeypatch, capsys, experiment, outcome):
    directory = next(ROOT.glob(f'实验{experiment:02}-*'))
    notebook = json.loads(next(directory.glob('*.ipynb')).read_text())
    cells = [c for c in notebook['cells'] if c['cell_type'] == 'code' and 'convert_notebook_to_webpdf(notebook_file' in ''.join(c['source'])]
    assert len(cells) == 1
    code = ''.join(cells[0]['source'])
    assert 'receipt = submit_pdf_report(' in code
    calls = []
    existing = tmp_path / 'report.pdf'
    existing.write_bytes(b'old PDF')

    def grade(path):
        calls.append('grade')
        return 100

    def generate(path, filename):
        calls.append('generate')
        if outcome == 'generation_failure':
            raise RuntimeError('generation failed')
        existing.write_bytes(b'new finished PDF')
        return existing

    def submit(path, info, experiment_number):
        calls.append('submit')
        assert calls == ['grade', 'generate', 'submit']
        assert path.read_bytes() == b'new finished PDF'
        assert experiment_number == experiment
        if outcome == 'submission_failure':
            raise RuntimeError('server unavailable')
        print('报告提交成功：回执编号 sub-test，版本 1。')
        return {'submission_id': 'sub-test', 'version': 1}

    generator = ModuleType('notebook2pdf')
    generator.convert_notebook_to_webpdf = generate
    uploader = ModuleType('report_submission')
    uploader.submit_pdf_report = submit
    monkeypatch.setitem(sys.modules, 'notebook2pdf', generator)
    monkeypatch.setitem(sys.modules, 'report_submission', uploader)
    monkeypatch.setattr(importlib, 'reload', lambda module: module)
    namespace = {f'testsuite{experiment}': SimpleNamespace(grade_all_tests=grade),
                 'receipt': {'submission_id': 'previous-run'}, 'notebook_file': 'saved.ipynb', 'stu_info': {'class_id':'c', 'student_id':'s', 'name':'N'}}
    if outcome == 'success':
        exec(compile(code, 'merged-notebook-cell', 'exec'), namespace)
        assert calls == ['grade', 'generate', 'submit']
        assert namespace['receipt']['submission_id'] == 'sub-test'
        assert '流程完成' in capsys.readouterr().out
    else:
        with pytest.raises(RuntimeError):
            exec(compile(code, 'merged-notebook-cell', 'exec'), namespace)
        output = capsys.readouterr().out
        assert '流程完成' not in output
        assert namespace['receipt'] is None
        if outcome == 'generation_failure':
            assert calls == ['grade', 'generate']
            assert existing.read_bytes() == b'old PDF'
        else:
            assert '报告提交失败' in output and '保留在' in output
            assert str(existing) in output
            assert existing.read_bytes() == b'new finished PDF'
