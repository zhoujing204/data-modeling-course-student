import os
import platform
import uuid
import nbformat
from nbconvert.exporters.webpdf import WebPDFExporter
from traitlets.config import Config
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


def _chinese_font_paths():
    """Return likely Chinese font locations for the current operating system."""
    system = platform.system()

    if system == "Windows":
        font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        return [
            os.path.join(font_dir, "msyh.ttc"),
            os.path.join(font_dir, "msyhbd.ttc"),
            os.path.join(font_dir, "simhei.ttf"),
            os.path.join(font_dir, "simkai.ttf"),
            os.path.join(font_dir, "simsun.ttc"),
        ]
    if system == "Darwin":
        return [
            os.path.expanduser("~/Library/Fonts/Arial Unicode MS.ttf"),
            os.path.expanduser("~/Library/Fonts/SimHei.ttf"),
            os.path.expanduser("~/Library/Fonts/SimSun.ttf"),
            "/Library/Fonts/Arial Unicode MS.ttf",
            "/Library/Fonts/Microsoft/SimHei.ttf",
            "/Library/Fonts/Microsoft/SimSun.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
        ]
    return [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ]


def _register_chinese_font(font_name="MyChineseFont"):
    """Register an installed Chinese font, with a portable CJK fallback."""
    for font_path in _chinese_font_paths():
        if not os.path.isfile(font_path):
            continue
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return font_name
        except Exception:
            # Some TTC files use PostScript outlines that ReportLab cannot load.
            # Continue looking instead of silently rendering Chinese as squares.
            continue

    cid_font_name = "STSong-Light"
    try:
        if cid_font_name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(UnicodeCIDFont(cid_font_name))
        return cid_font_name
    except Exception as error:
        raise RuntimeError(
            "No usable Chinese PDF font was found. Install a Chinese TrueType font."
        ) from error


def add_header_footer(input_pdf_path, output_pdf_path, font_name="MyChineseFont"):

    header_text = "计算机科学与工程学院数学建模实验报告"
    footer_text = "页码: 第 {} 页 / 共 {} 页"

    chinese_font = _register_chinese_font(font_name)

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        can.setFont(chinese_font, 10)

        can.drawCentredString(page_width / 2, page_height - 22, header_text)
        can.setLineWidth(1)
        can.line(50, page_height - 32, page_width - 50, page_height - 32)

        can.setFont(chinese_font, 8)

        footer_str = footer_text.format(page_num + 1, len(reader.pages))
        can.drawCentredString(page_width / 2, 20, footer_str)

        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

    os.replace(output_pdf_path, input_pdf_path)


def convert_notebook_to_webpdf(notebook_path, output_pdf):
    """Return the completed PDF path, or raise without replacing an existing report.

    Rendering, header/footer stamping and validation all finish before the final
    atomic rename. Callers can submit the returned file immediately on success.
    """
    temporary_paths = []
    print("正在渲染报告并添加页眉页脚，请稍候……")
    try:
        if not notebook_path:
            raise ValueError("未找到 Notebook 路径，请先保存文件并重新运行实验准备单元格。")
        output_path = Path(output_pdf).expanduser().resolve()
        if output_path.suffix.lower() != ".pdf":
            raise ValueError("报告文件名必须以 .pdf 结尾。")
        token = uuid.uuid4().hex
        rendered_path = output_path.with_name(f".{output_path.name}.{token}.render.pdf")
        stamped_path = output_path.with_name(f".{output_path.name}.{token}.footer.pdf")
        temporary_paths = [rendered_path, stamped_path]

        with open(notebook_path, "r", encoding="utf-8") as source:
            notebook = nbformat.read(source, as_version=4)
        nbformat.validate(notebook)
        config = Config()
        config.WebPDFExporter.allow_chromium_download = True
        config.WebPDFExporter.wait_until = "domcontentloaded"
        config.WebPDFExporter.timeout = 180000
        config.WebPDFExporter.script = """
        () => new Promise(resolve => setTimeout(resolve, 3000))
        """
        pdf_data, _ = WebPDFExporter(config=config).from_notebook_node(notebook)
        if not PdfReader(BytesIO(pdf_data)).pages:
            raise ValueError("转换结果没有页面，未生成可提交的 PDF。")

        with rendered_path.open("wb") as report:
            report.write(pdf_data)
            report.flush()
            os.fsync(report.fileno())
        add_header_footer(str(rendered_path), str(stamped_path))
        with rendered_path.open("rb") as report:
            page_count = len(PdfReader(report).pages)
        if not page_count:
            raise ValueError("页眉页脚处理后没有有效页面。")
        size_kb = rendered_path.stat().st_size / 1024
        os.replace(rendered_path, output_path)
    except Exception as error:
        print(f"PDF 报告生成失败，已停止后续提交。原因：{error}")
        raise RuntimeError("PDF 报告生成失败；本次未提交到 LabDrop。") from error
    finally:
        for temporary_path in temporary_paths:
            temporary_path.unlink(missing_ok=True)

    print(f"PDF 报告生成成功：{page_count} 页，{size_kb:.1f} KB。")
    print(f"本地文件：{output_path}")
    return output_path


if __name__ == "__main__":
    # 示例
    convert_notebook_to_webpdf("example.ipynb", "output.pdf")
