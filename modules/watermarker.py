import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import os

def create_text_watermark(text):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name, pagesize=letter)
    c.setFont("Helvetica", 40)
    c.setFillGray(0.5, 0.5)
    c.saveState()
    c.translate(300, 500)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    return temp.name

def add_watermark(input_pdf_path, watermark_pdf_path, output_pdf_path):
    try:
        with open(input_pdf_path, 'rb') as input_file, open(watermark_pdf_path, 'rb') as watermark_file:
            input_reader = PyPDF2.PdfReader(input_file)
            watermark_reader = PyPDF2.PdfReader(watermark_file)
            watermark_page = watermark_reader.pages[0]

            writer = PyPDF2.PdfWriter()
            for page in input_reader.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)

            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)

        return True, "✅ Watermark added successfully."
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

