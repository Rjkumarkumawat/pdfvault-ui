# modules/merger.py

import PyPDF2

def merge_pdfs(file_paths, output_path):
    try:
        merger = PyPDF2.PdfMerger()
        for file in file_paths:
            merger.append(file)
        merger.write(output_path)
        merger.close()
        return True, "PDFs merged successfully."
    except Exception as e:
        return False, f"Error: {e}"

