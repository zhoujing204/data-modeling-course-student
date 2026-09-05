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
