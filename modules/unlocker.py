# modules/unlocker.py

import PyPDF2

def unlock_pdf(input_path, output_path, password):
    try:
        with open(input_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            if reader.is_encrypted:
                try:
                    reader.decrypt(password)
                except Exception:
                    return False, "Incorrect password or unable to decrypt."

            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, 'wb') as f_out:
                writer.write(f_out)

        return True, "PDF unlocked successfully."
    except Exception as e:
        return False, f"Error: {e}"

