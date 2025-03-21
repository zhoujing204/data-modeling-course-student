import os

import nbformat
import pdfkit
from nbconvert import HTMLExporter
from nbconvert.exporters.webpdf import WebPDFExporter
from traitlets.config import Config
import time
from tqdm import tqdm
import threading

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
            print(f"Successfully converted {html_path} to {output_path}")
        else:
            print(f"Error or timeout converting {html_path} to PDF")

    except Exception as e:
        print(f"Error converting {html_path} to PDF: {str(e)}")



# def convert_notebook_to_webpdf(notebook_path, output_pdf):
#     # Read the .ipynb file
#     with open(notebook_path, "r", encoding="utf-8") as f:
#         nb = nbformat.read(f, as_version=4)

#     # Create a configuration that allows Chromium to be downloaded if needed.
#     c = Config()
#     c.WebPDFExporter.allow_chromium_download = True

#     # Create the exporter using the configuration.
#     exporter = WebPDFExporter(config=c)

#     # Convert the notebook to a WebPDF
#     pdf_data, resources = exporter.from_notebook_node(nb)

#     # Write the PDF data to an output file.
#     with open(output_pdf, "wb") as f:
#         f.write(pdf_data)

#     print("Conversion complete:", output_pdf)

# def notebook_to_html(notebook_path, html_path):
#     try:
#         # Load the notebook
#         with open(notebook_path, 'r', encoding='utf-8') as f:
#             notebook_content = nbformat.read(f, as_version=4)

#         # Export the notebook to HTML
#         html_exporter = HTMLExporter()
#         (body, resources) = html_exporter.from_notebook_node(notebook_content)

#         # Save the HTML output to a file
#         with open(html_path, 'w', encoding='utf-8') as f:
#             f.write(body)

#         print(f"Notebook successfully converted to HTML: {html_path}")

#     except Exception as e:
#         print(f"Error converting notebook to HTML: {str(e)}")


# def html_to_pdf(html_path, output_path):
#     try:
#         # Options for wkhtmltopdf
#         options = {
#             'no-images': '',  # Disable images if they’re causing issues
#             'disable-external-links': '',
#             'page-size': 'A4',
#             'margin-top': '0.75in',
#             'margin-right': '0.75in',
#             'margin-bottom': '0.75in',
#             'margin-left': '0.75in',
#             'encoding': "UTF-8",
#             'header-center': '长沙学院计算机科学与工程学院实验报告',  # Add custom header text
#             'header-font-size': '10',  # Font size of the header
#             'header-line': '',  # Add a horizontal line beneath the header
#             'header-spacing': '5',  # Spacing between the header and content
#             'footer-center': 'Page [page] of [topage]',  # Footer text with page numbers
#             'footer-font-size': '10',  # Footer font size
#             'footer-spacing': '5',    # Spacing between footer and page content
#         }
#         pdfkit.from_file(html_path, output_path, options=options)
#         print(f"Successfully converted {html_path} to {output_path}")

#         # Delete the temporary HTML file after conversion
#         # if os.path.exists(html_path):
#         #     os.remove(html_path)
#         #     print(f"Deleted temporary file: {html_path}")

#     except OSError as os_error:
#         print(f"Error: Ensure wkhtmltopdf is installed and accessible. Details: {str(os_error)}")

#     except Exception as e:
#         print(f"Error converting file: {str(e)}")


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
