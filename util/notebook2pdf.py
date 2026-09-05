import os
import platform
import uuid
import nbformat
from nbconvert.exporters.webpdf import WebPDFExporter
from traitlets.config import Config
import time
from tqdm import tqdm
import threading
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
        output_path = os.path.abspath(output_pdf)
        temporary_pdf = os.path.join(
            os.path.dirname(output_path),
            f".{os.path.basename(output_path)}.{uuid.uuid4().hex}.tmp.pdf",
        )
        add_header_footer(output_path, temporary_pdf)
        print(f"\n成功生成报告文件: {output_pdf}")
    else:
        print(f"\n转换失败: {notebook_path}")


if __name__ == "__main__":
    # 示例
    convert_notebook_to_webpdf("example.ipynb", "output.pdf")
