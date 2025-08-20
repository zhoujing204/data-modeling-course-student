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

# def add_header_footer(input_pdf_path, output_pdf_path, font_name="MyChineseFont"):
#     font_path = r"C:\\Windows\\Fonts\\simsun.ttc"
#     header_text = "计算机科学与工程学院数学建模实验报告"
#     footer_text = "页码: 第 {} 页 / 共 {} 页"
#     # 注册自定义中文字体
#     pdfmetrics.registerFont(TTFont(font_name, font_path))

#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]
#         packet = BytesIO()
#         can = canvas.Canvas(packet, pagesize=letter)

#         # 页眉
#         can.setFont(font_name, 10)
#         can.drawCentredString(letter[0] / 2, 770, header_text)

#         # 在页眉下方添加实线
#         can.setLineWidth(1)  # 设置线条宽度
#         can.line(50, 760, letter[0] - 50, 760)  # 绘制实线 (x1, y1, x2, y2)

#         # 页脚
#         can.setFont(font_name, 8)
#         footer_str = footer_text.format(page_num + 1, len(reader.pages))
#         can.drawCentredString(297, 20, footer_str)
#         can.save()
#         packet.seek(0)
#         new_pdf = PdfReader(packet)
#         page.merge_page(new_pdf.pages[0])
#         writer.add_page(page)

#     with open(output_pdf_path, 'wb') as output_file:
#         writer.write(output_file)

#     # 删除原文件
#     os.remove(input_pdf_path)
#     # 重命名输出文件为原输入文件名称
#     os.rename(output_pdf_path, input_pdf_path)
#     # print(f"已成功添加中文页眉和页脚，并覆盖保存为 {input_pdf_path}")

def add_header_footer(input_pdf_path, output_pdf_path, font_name="MyChineseFont"):
    """
    为PDF文件添加中文页眉和页脚, 支持Windows和macOS系统

    参数:
    input_pdf_path: 输入PDF文件路径
    output_pdf_path: 输出PDF文件路径
    font_name: 字体名称
    """

    def get_chinese_font_path():
        """根据操作系统获取中文字体路径, 优先选择TTF格式字体"""
        system = platform.system()

        if system == "Windows":
            # Windows系统字体路径（优先TTF格式）
            font_paths = [
                r"C:\Windows\Fonts\simhei.ttf",      # 黑体 (TTF)
                r"C:\Windows\Fonts\simkai.ttf",      # 楷体 (TTF)
                r"C:\Windows\Fonts\simsun.ttc",      # 宋体 (TTC)
                r"C:\Windows\Fonts\msyh.ttc",        # 微软雅黑 (TTC)
            ]
        elif system == "Darwin":  # macOS
            # macOS系统字体路径（优先TTF格式，避免TTC格式）
            font_paths = [
                # 首先尝试用户安装的TTF字体
                os.path.expanduser("~/Library/Fonts/SimHei.ttf"),         # 黑体
                os.path.expanduser("~/Library/Fonts/SimSun.ttf"),         # 宋体
                os.path.expanduser("~/Library/Fonts/KaiTi.ttf"),          # 楷体
                os.path.expanduser("~/Library/Fonts/Arial Unicode MS.ttf"), # Arial Unicode MS

                # 系统字体中的TTF格式
                "/Library/Fonts/Arial Unicode MS.ttf",                    # Arial Unicode MS
                "/System/Library/Fonts/STHeiti Medium.ttc",               # 华文黑体（作为备选）

                # 如果有安装Office等软件的字体
                "/Library/Fonts/Microsoft/SimHei.ttf",
                "/Library/Fonts/Microsoft/SimSun.ttf",

                # 最后尝试TTC格式（可能会失败）
                "/System/Library/Fonts/PingFang.ttc",                     # 苹方字体
                "/System/Library/Fonts/Songti.ttc",                       # 宋体
            ]
        else:
            # Linux或其他系统
            font_paths = [
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/chinese/TrueType/uming.ttc",
                "/usr/share/fonts/chinese/TrueType/ukai.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",        # 备选字体
            ]

        # 查找存在的字体文件
        for font_path in font_paths:
            if os.path.exists(font_path):
                print(f"找到字体文件: {font_path}")
                return font_path

        # 如果没有找到中文字体，返回None（将使用默认字体）
        print(f"警告: 在{system}系统上未找到可用的中文字体文件")
        return None

    def test_font_registration(font_path, font_name):
        """测试字体注册是否成功"""
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            print(f"成功注册字体: {font_path}")
            return True
        except Exception as e:
            print(f"字体注册失败 {font_path}: {e}")
            return False

    header_text = "计算机科学与工程学院数学建模实验报告"
    footer_text = "页码: 第 {} 页 / 共 {} 页"

    # 获取字体路径并尝试注册
    font_path = get_chinese_font_path()
    use_chinese_font = False

    if font_path:
        use_chinese_font = test_font_registration(font_path, font_name)


    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # 设置字体
            if use_chinese_font:
                can.setFont(font_name, 10)

            else:
                can.setFont("Helvetica", 10)  # 默认字体


            # 页眉
            can.drawCentredString(letter[0] / 2, 770, header_text)

            # 在页眉下方添加实线
            can.setLineWidth(1)
            can.line(50, 760, letter[0] - 50, 760)

            # 页脚
            if use_chinese_font:
                can.setFont(font_name, 8)
            else:
                can.setFont("Helvetica", 8)  # 默认字体

            footer_str = footer_text.format(page_num + 1, len(reader.pages))
            can.drawCentredString(letter[0] / 2, 20, footer_str)

            can.save()
            packet.seek(0)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])
            writer.add_page(page)

        # 写入输出文件
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

        # 删除原文件并重命名
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)
        os.rename(output_pdf_path, input_pdf_path)


    except Exception as e:
        print(f"处理PDF文件时出错: {e}")
        # 如果出错，确保不删除原文件
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
        raise

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
