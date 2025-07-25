# modules/splitter.py

import PyPDF2
import os

def split_pdf(input_path, output_folder):
    try:
        with open(input_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            os.makedirs(output_folder, exist_ok=True)

            for i, page in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)

                output_path = os.path.join(output_folder, f"page_{i + 1}.pdf")
                with open(output_path, 'wb') as out_file:
                    writer.write(out_file)

        return True, "PDF split into individual pages successfully."
    except Exception as e:
        return False, f"Error: {e}"

