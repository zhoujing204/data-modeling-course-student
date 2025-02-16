from nbconvert import HTMLExporter
import nbformat
import pdfkit

import nbformat
from traitlets.config import Config
from nbconvert.exporters.webpdf import WebPDFExporter

def convert_notebook_to_webpdf(notebook_path, output_pdf):
    # Read the .ipynb file
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Create a configuration that allows Chromium to be downloaded if needed.
    c = Config()
    c.WebPDFExporter.allow_chromium_download = True

    # Create the exporter using the configuration.
    exporter = WebPDFExporter(config=c)

    # Convert the notebook to a WebPDF
    pdf_data, resources = exporter.from_notebook_node(nb)

    # Write the PDF data to an output file.
    with open(output_pdf, "wb") as f:
        f.write(pdf_data)

    print("Conversion complete:", output_pdf)

def notebook_to_html(notebook_path, html_path):
    try:
        # Load the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Export the notebook to HTML
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(notebook_content)

        # Save the HTML output to a file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(body)

        print(f"Notebook successfully converted to HTML: {html_path}")

    except Exception as e:
        print(f"Error converting notebook to HTML: {str(e)}")


def html_to_pdf(html_path, output_path):
    try:
        # Options for wkhtmltopdf
        options = {
            'no-images': '',  # Disable images if they’re causing issues
            'disable-external-links': '',
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'header-center': '长沙学院计算机科学与工程学院实验报告',  # Add custom header text
            'header-font-size': '10',  # Font size of the header
            'header-line': '',  # Add a horizontal line beneath the header
            'header-spacing': '5',  # Spacing between the header and content
            'footer-center': 'Page [page] of [topage]',  # Footer text with page numbers
            'footer-font-size': '10',  # Footer font size
            'footer-spacing': '5',    # Spacing between footer and page content
        }
        pdfkit.from_file(html_path, output_path, options=options)
        print(f"Successfully converted {html_path} to {output_path}")

    except OSError as os_error:
        print(f"Error: Ensure wkhtmltopdf is installed and accessible. Details: {str(os_error)}")

    except Exception as e:
        print(f"Error converting file: {str(e)}")

# Example usage
# notebook_file = "notebook.ipynb"
# html_file = "notebook.html"
# pdf_file = "output.pdf"

# notebook_to_html(notebook_file, html_file)
# html_to_pdf(html_file, pdf_file)