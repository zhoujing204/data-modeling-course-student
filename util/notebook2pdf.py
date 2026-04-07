import os
import platform
import nbformat
from nbconvert.exporters.webpdf import WebPDFExporter
from traitlets.config import Config
import time
from tqdm import tqdm
import threading
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


def add_header_footer(input_pdf_path, output_pdf_path, font_name="MyChineseFont"):
    def get_chinese_font_path():
        system = platform.system()

        if system == "Windows":
            font_paths = [
                r"C:\\Windows\\Fonts\\simhei.ttf",
                r"C:\\Windows\\Fonts\\simkai.ttf",
                r"C:\\Windows\\Fonts\\simsun.ttc",
                r"C:\\Windows\\Fonts\\msyh.ttc",
            ]
        elif system == "Darwin":
            font_paths = [
                os.path.expanduser("~/Library/Fonts/SimHei.ttf"),
                os.path.expanduser("~/Library/Fonts/SimSun.ttf"),
                os.path.expanduser("~/Library/Fonts/KaiTi.ttf"),
                os.path.expanduser("~/Library/Fonts/Arial Unicode MS.ttf"),
                "/Library/Fonts/Arial Unicode MS.ttf",
                "/Library/Fonts/Microsoft/SimHei.ttf",
                "/Library/Fonts/Microsoft/SimSun.ttf",
                "/System/Library/Fonts/PingFang.ttc",
            ]
        else:
            font_paths = [
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]

        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path
        return None

    def test_font_registration(font_path, font_name):
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            return True
        except Exception:
            return False

    header_text = "计算机科学与工程学院数学建模实验报告"
    footer_text = "页码: 第 {} 页 / 共 {} 页"

    font_path = get_chinese_font_path()
    use_chinese_font = False

    if font_path:
        use_chinese_font = test_font_registration(font_path, font_name)

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        if use_chinese_font:
            can.setFont(font_name, 10)
        else:
            can.setFont("Helvetica", 10)

        can.drawCentredString(letter[0] / 2, 770, header_text)
        can.setLineWidth(1)
        can.line(50, 760, letter[0] - 50, 760)

        if use_chinese_font:
            can.setFont(font_name, 8)
        else:
            can.setFont("Helvetica", 8)

        footer_str = footer_text.format(page_num + 1, len(reader.pages))
        can.drawCentredString(letter[0] / 2, 20, footer_str)

        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

    os.remove(input_pdf_path)
    os.rename(output_pdf_path, input_pdf_path)


def convert_notebook_to_webpdf(notebook_path, output_pdf):
    pbar = tqdm(total=100, desc='Notebook to PDF', unit='%')

    progress = 0
    max_progress = 95
    duration = 15
    tick = duration / max_progress

    conversion_complete = threading.Event()
    conversion_success = {"ok": False}

    def convert():
        try:
            with open(notebook_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)

            c = Config()
            c.WebPDFExporter.allow_chromium_download = True

            # ✅ 核心修复（避免 networkidle 超时）
            c.WebPDFExporter.wait_until = "domcontentloaded"
            c.WebPDFExporter.timeout = 180000

            # ✅ 给 JS 渲染留时间（解决 plotly 等）
            c.WebPDFExporter.script = """
            () => new Promise(resolve => setTimeout(resolve, 3000))
            """

            exporter = WebPDFExporter(config=c)
            pdf_data, _ = exporter.from_notebook_node(nb)

            with open(output_pdf, "wb") as fout:
                fout.write(pdf_data)

            conversion_success["ok"] = True

        except Exception as e:
            print(f"Conversion error: {e}")

        finally:
            conversion_complete.set()

    threading.Thread(target=convert, daemon=True).start()

    while progress < max_progress and not conversion_complete.is_set():
        time.sleep(tick)
        progress += 1
        pbar.update(1)

    while not conversion_complete.is_set():
        time.sleep(0.2)

    if pbar.n < 100:
        pbar.update(100 - pbar.n)
    pbar.close()

    if conversion_success["ok"] and os.path.exists(output_pdf):
        add_header_footer(output_pdf, "temp.pdf")
        print(f"\n成功生成报告文件: {output_pdf}")
    else:
        print(f"\n转换失败: {notebook_path}")


if __name__ == "__main__":
    # 示例
    convert_notebook_to_webpdf("example.ipynb", "output.pdf")
