from io import BytesIO
from pathlib import Path

import nbformat
import pytest
from util import notebook2pdf
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from util.notebook2pdf import add_header_footer


def test_header_and_footer_preserve_chinese_text(tmp_path):
    report_path = tmp_path / "report.pdf"
    temporary_path = tmp_path / "stamped.pdf"

    report = canvas.Canvas(str(report_path), pagesize=letter)
    report.setFont("Helvetica", 12)
    report.drawString(72, 700, "Notebook report body")
    report.save()

    add_header_footer(report_path, temporary_path)

    extracted_text = "\n".join(
        page.extract_text() or "" for page in PdfReader(report_path).pages
    )
    assert "计算机科学与工程学院数学建模实验报告" in extracted_text
    assert "页码: 第 1 页 / 共 1 页" in extracted_text



def _pdf_bytes():
    stream = BytesIO()
    report = canvas.Canvas(stream, pagesize=letter)
    report.drawString(72, 700, 'New report')
    report.save()
    return stream.getvalue()


def _fake_exporter(monkeypatch, payload=None, error=None):
    class Exporter:
        def __init__(self, **kwargs):
            pass

        def from_notebook_node(self, notebook):
            if error:
                raise error
            return payload if payload is not None else _pdf_bytes(), {}

    monkeypatch.setattr(notebook2pdf, 'WebPDFExporter', Exporter)


def _notebook(tmp_path):
    path = tmp_path / 'experiment.ipynb'
    nbformat.write(nbformat.v4.new_notebook(), path)
    return path


def test_generation_returns_only_after_new_pdf_has_headers(tmp_path, monkeypatch, capsys):
    source = _notebook(tmp_path)
    target = tmp_path / 'report.pdf'
    target.write_bytes(b'old report')
    _fake_exporter(monkeypatch)
    original = notebook2pdf.add_header_footer

    def stamp(staged, temporary):
        assert target.read_bytes() == b'old report'
        assert Path(staged) != target
        original(staged, temporary)

    monkeypatch.setattr(notebook2pdf, 'add_header_footer', stamp)
    result = notebook2pdf.convert_notebook_to_webpdf(source, target)
    assert result == target.resolve()
    text = ''.join(page.extract_text() or '' for page in PdfReader(result).pages)
    assert 'New report' in text and '页码: 第 1 页 / 共 1 页' in text
    assert not list(tmp_path.glob('.*.pdf'))
    assert 'PDF 报告生成成功' in capsys.readouterr().out


@pytest.mark.parametrize('failure', ['export', 'invalid_pdf', 'empty_pdf', 'footer', 'publish', 'missing_notebook'])
def test_failure_preserves_old_pdf_and_raises(tmp_path, monkeypatch, capsys, failure):
    source = _notebook(tmp_path)
    target = tmp_path / 'report.pdf'
    target.write_bytes(b'old report')
    _fake_exporter(monkeypatch)
    if failure == 'export':
        _fake_exporter(monkeypatch, error=RuntimeError('renderer failed'))
    elif failure == 'invalid_pdf':
        _fake_exporter(monkeypatch, payload=b'invalid PDF')
    elif failure == 'empty_pdf':
        from PyPDF2 import PdfWriter
        empty = BytesIO()
        PdfWriter().write(empty)
        _fake_exporter(monkeypatch, payload=empty.getvalue())
    elif failure == 'footer':
        def fail(*args):
            raise OSError('cannot add footer')
        monkeypatch.setattr(notebook2pdf, 'add_header_footer', fail)
    elif failure == 'publish':
        replace = notebook2pdf.os.replace
        def fail_publish(src, dst):
            if Path(dst) == target:
                raise OSError('cannot publish PDF')
            return replace(src, dst)
        monkeypatch.setattr(notebook2pdf.os, 'replace', fail_publish)
    elif failure == 'missing_notebook':
        source = None
    with pytest.raises(RuntimeError, match='本次未提交'):
        notebook2pdf.convert_notebook_to_webpdf(source, target)
    assert target.read_bytes() == b'old report'
    assert not list(tmp_path.glob('.*.pdf'))
    output = capsys.readouterr().out
    assert '生成失败，已停止后续提交' in output
    assert '生成成功' not in output
