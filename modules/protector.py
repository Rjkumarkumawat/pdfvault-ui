# modules/protector.py

import os
import PyPDF2
from PyPDF2.errors import PdfReadError

def protect_pdf(input_path, output_path, password):
    try:
        with open(input_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            return True, "Password protection applied successfully."
    except FileNotFoundError:
        return False, "Input file not found."
    except PdfReadError:
        return False, "Invalid or corrupted PDF file."
    except Exception as e:
        return False, f"Unexpected error: {e}"

