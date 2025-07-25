import streamlit as st
import os
import zipfile
from modules.protector import protect_pdf
from modules.unlocker import unlock_pdf
from modules.merger import merge_pdfs
from modules.splitter import split_pdf
from modules.watermarker import add_watermark, create_text_watermark

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("protected", exist_ok=True)
os.makedirs("unlocked", exist_ok=True)
os.makedirs("split", exist_ok=True)
os.makedirs("watermarked", exist_ok=True)

st.set_page_config(page_title="PDFVault-UI", page_icon="🔐")
st.title("🔐 PDFVault-UI")
st.sidebar.title("Tools")

tool = st.sidebar.radio("Select a PDF tool:", [
    "Protect PDF",
    "Unlock PDF",
    "Merge PDFs",
    "Split PDF",
    "Add Watermark"
])

# 🔒 Module 1: Protect PDF
if tool == "Protect PDF":
    st.subheader("🔒 Password Protect PDF")
    file = st.file_uploader("Upload PDF to protect", type="pdf", key="protect")
    password = st.text_input("Enter password to apply", type="password")
    if file and password:
        input_path = os.path.join("uploads", file.name)
        output_path = os.path.join("protected", f"protected_{file.name}")
        with open(input_path, "wb") as f:
            f.write(file.read())
        if st.button("🚀 Protect PDF"):
            success, message = protect_pdf(input_path, output_path, password)
            if success:
                st.success(message)
                with open(output_path, "rb") as f_out:
                    st.download_button("📥 Download Protected PDF", f_out, file_name=f"protected_{file.name}", mime="application/pdf")
            else:
                st.error(message)

# 🔓 Module 2: Unlock PDF
elif tool == "Unlock PDF":
    st.subheader("🔓 Unlock a Password-Protected PDF")
    file = st.file_uploader("Upload encrypted PDF", type="pdf", key="unlock")
    password = st.text_input("Enter password to unlock", type="password")
    if file and password:
        input_path = os.path.join("uploads", file.name)
        output_path = os.path.join("unlocked", f"unlocked_{file.name}")
        with open(input_path, "wb") as f:
            f.write(file.read())
        if st.button("🔓 Unlock PDF"):
            success, message = unlock_pdf(input_path, output_path, password)
            if success:
                st.success(message)
                with open(output_path, "rb") as f_out:
                    st.download_button("📥 Download Unlocked PDF", f_out, file_name=f"unlocked_{file.name}", mime="application/pdf")
            else:
                st.error(message)

# 📎 Module 3: Merge PDFs
elif tool == "Merge PDFs":
    st.subheader("📎 Merge Multiple PDF Files")
    uploaded_files = st.file_uploader("Upload 2 or more PDFs", type="pdf", accept_multiple_files=True)
    if uploaded_files and len(uploaded_files) >= 2:
        file_paths = []
        output_path = os.path.join("uploads", "merged_output.pdf")
        for uploaded_file in uploaded_files:
            temp_path = os.path.join("uploads", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())
            file_paths.append(temp_path)
        if st.button("🛠️ Merge PDFs"):
            success, message = merge_pdfs(file_paths, output_path)
            if success:
                st.success(message)
                with open(output_path, "rb") as f_out:
                    st.download_button("📥 Download Merged PDF", f_out, file_name="merged_output.pdf", mime="application/pdf")
            else:
                st.error(message)

# ✂️ Module 4: Split PDF
elif tool == "Split PDF":
    st.subheader("✂️ Split PDF into Individual Pages")
    file = st.file_uploader("Upload PDF to split", type="pdf", key="split")
    if file:
        input_path = os.path.join("uploads", file.name)
        split_dir = os.path.join("split", file.name.replace(".pdf", ""))
        os.makedirs(split_dir, exist_ok=True)
        with open(input_path, "wb") as f:
            f.write(file.read())
        if st.button("✂️ Split PDF"):
            success, message = split_pdf(input_path, split_dir)
            if success:
                zip_path = f"{split_dir}.zip"
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for page_file in os.listdir(split_dir):
                        full_path = os.path.join(split_dir, page_file)
                        zipf.write(full_path, page_file)
                st.success(message)
                with open(zip_path, "rb") as z:
                    st.download_button("📥 Download All Pages (ZIP)", z, file_name=os.path.basename(zip_path), mime="application/zip")
            else:
                st.error(message)

# 📝 Module 5: Add Watermark (PDF or Text)
elif tool == "Add Watermark":
    st.subheader("📝 Add Watermark to PDF")
    watermark_type = st.radio("Select watermark type", ["Upload PDF", "Enter Text"])
    base_pdf = st.file_uploader("Upload PDF to watermark", type="pdf", key="wm_base")

    watermark_path = None

    if watermark_type == "Upload PDF":
        watermark_file = st.file_uploader("Upload 1-page Watermark PDF", type="pdf", key="wm_upload")
        if watermark_file:
            watermark_path = os.path.join("uploads", f"watermark_{watermark_file.name}")
            with open(watermark_path, "wb") as f:
                f.write(watermark_file.read())

    elif watermark_type == "Enter Text":
        text_input = st.text_input("Enter watermark text")
        if text_input:
            watermark_path = create_text_watermark(text_input)

    if base_pdf and watermark_path:
        base_path = os.path.join("uploads", base_pdf.name)
        output_path = os.path.join("watermarked", f"watermarked_{base_pdf.name}")
        with open(base_path, "wb") as f:
            f.write(base_pdf.read())

        if st.button("🖌️ Apply Watermark"):
            success, message = add_watermark(base_path, watermark_path, output_path)
            if success:
                st.success(message)
                with open(output_path, "rb") as result:
                    st.download_button("📥 Download Watermarked PDF", result, file_name=f"watermarked_{base_pdf.name}", mime="application/pdf")
            else:
                st.error(message)

# 👣 Footer
st.markdown(
    '''<hr>
    <div style="text-align: center; font-size: 14px; color: gray;">
        🚀 Created by <strong>Rajkumar Kumawat</strong> | Tool: <em>PDFVault-UI</em> | © 2025
    </div>''',
    unsafe_allow_html=True
)

