import os
import nbformat
import pdfkit
from nbconvert import HTMLExporter
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
    font_path = r"C:\\Windows\\Fonts\\simsun.ttc"
    header_text = "计算机科学与工程学院数学建模实验报告"
    footer_text = "页码: 第 {} 页 / 共 {} 页"
    # 注册自定义中文字体
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # 页眉
        can.setFont(font_name, 10)
        can.drawCentredString(letter[0] / 2, 770, header_text)

        # 在页眉下方添加实线
        can.setLineWidth(1)  # 设置线条宽度
        can.line(50, 760, letter[0] - 50, 760)  # 绘制实线 (x1, y1, x2, y2)

        # 页脚
        can.setFont(font_name, 8)
        footer_str = footer_text.format(page_num + 1, len(reader.pages))
        can.drawCentredString(297, 20, footer_str)
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

    # 删除原文件
    os.remove(input_pdf_path)
    # 重命名输出文件为原输入文件名称
    os.rename(output_pdf_path, input_pdf_path)
    # print(f"已成功添加中文页眉和页脚，并覆盖保存为 {input_pdf_path}")

def html_to_pdf(html_path, output_path):
    try:
        # Options for wkhtmltopdf
        options = {
            'no-images': '',
            'disable-external-links': '',
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'header-center': '长沙学院计算机科学与工程学院实验报告',
            'header-font-size': '10',
            'header-line': '',
            'header-spacing': '5',
            'footer-center': 'Page [page] of [topage]',
            'footer-font-size': '10',
            'footer-spacing': '5',
        }

        # Create progress bar
        pbar = tqdm(total=100, desc="Converting to PDF", unit="%")
        start_time = time.time()

        # Estimate total time based on file size (adjust constant based on experience)
        file_size = os.path.getsize(html_path)
        estimated_total_time = max(5, min(40, file_size / 100000))  # Between 5-30 seconds

        # Flag to indicate conversion is complete
        conversion_complete = threading.Event()

        # Start the conversion in a separate thread
        def convert():
            pdfkit.from_file(html_path, output_path, options=options)
            conversion_complete.set()

        threading.Thread(target=convert, daemon=True).start()

        # Monitor and update progress while conversion is running
        progress = 0
        while not conversion_complete.is_set() and progress < 100:
            elapsed = time.time() - start_time

            # Calculate progress based on elapsed time
            new_progress = min(95, int((elapsed / estimated_total_time) * 100))

            if new_progress > progress:
                pbar.update(new_progress - progress)
                progress = new_progress

                # Estimate remaining time
                remaining = estimated_total_time - elapsed
                if remaining > 0:
                    pbar.set_postfix({"Remaining": f"{remaining:.1f}s"})

            time.sleep(0.1)

            # Check if output file exists and is growing
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path)
                # Additional logic could be added here to refine progress based on output size

        # Wait for conversion to complete (with timeout)
        conversion_complete.wait(timeout=max(60, estimated_total_time * 2))

        # Complete the progress bar
        pbar.update(100 - progress)
        pbar.close()

        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"成功生成实验报告文件: {output_path}")
        else:
            print(f"Error or timeout converting {html_path} to PDF")

    except Exception as e:
        print(f"Error converting {html_path} to PDF: {str(e)}")


def convert_notebook_to_webpdf(notebook_path, output_pdf):
    pbar = tqdm(total=100, desc='Notebook to PDF', unit='%')

    progress = 0
    max_progress = 99
    duration = 12  # 12秒内达到99%
    tick = duration / max_progress  # 每1%用时

    conversion_complete = threading.Event()

    # 启动实际转换线程
    def convert():
        try:
            with open(notebook_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
            c = Config()
            c.WebPDFExporter.allow_chromium_download = True
            exporter = WebPDFExporter(config=c)
            pdf_data, resources = exporter.from_notebook_node(nb)
            with open(output_pdf, "wb") as fout:
                fout.write(pdf_data)
        except Exception as e:
            print(f"Conversion error: {e}")
        conversion_complete.set()

    threading.Thread(target=convert, daemon=True).start()

    # 进度递增至99%
    while progress < max_progress and not conversion_complete.is_set():
        time.sleep(tick)
        progress += 1
        pbar.update(1)

    # 若转换还没好，需继续等待
    while not conversion_complete.is_set():
        time.sleep(0.1)

    # 最后补到100%
    if pbar.n < 100:
        pbar.update(100 - pbar.n)
    pbar.close()

    if os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
        add_header_footer(output_pdf, "temp.pdf")
        print(f"\n成功生成报告文件: {output_pdf}")
    else:
        print(f"\n转换文件 {notebook_path} 到PDF格式出现错误")


def notebook_to_html(notebook_path, html_path):
    try:
        # Load the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Export the notebook to HTML
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(notebook_content)

        # Add styles for table (to ensure table borders are visible)
        table_styles = """
        <style>
        table {
            margin: 0 auto;
            border-collapse: collapse;
            width: 100%;
        }
        table, th, td {
            border: 1px solid black;
        }
        td, th {
            padding: 8px;
            text-align: left;
        }
        </style>
        """
        body = table_styles + body  # Prepend the style block to the HTML content

        # Save the updated HTML output to a file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(body)

        print(f"Notebook successfully converted to HTML with table styles: {html_path}")

    except Exception as e:
        print(f"Error converting notebook to HTML: {str(e)}")
