import streamlit as st
from pdf2docx import Converter
import os
import tempfile

# Page configurations
st.set_page_config(page_title="PDF to Word Converter", page_icon="📄")

st.title("📄 PDF to Word Converter")
st.write("ඔබේ PDF එක Upload කරන්න. අපි එය Word (.docx) බවට පත් කර දෙන්නෙමු.")

# File uploader
uploaded_file = st.file_uploader("PDF එකක් තෝරන්න", type="pdf")

if uploaded_file is not None:
    # Creating a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name
        
    docx_path = pdf_path.replace(".pdf", ".docx")

    if st.button("Convert Now"):
        with st.spinner('පරිවර්තනය වෙමින් පවතී...'):
            try:
                # Actual conversion logic
                cv = Converter(pdf_path)
                cv.convert(docx_path, start=0, end=None)
                cv.close()

                # Open the converted file to allow download
                with open(docx_path, "rb") as word_file:
                    st.download_button(
                        label="Download Word Document",
                        data=word_file,
                        file_name=uploaded_file.name.replace(".pdf", ".docx"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.success("සාර්ථකයි! දැන් Download කරන්න.")
            except Exception as e:
                st.error(f"දෝෂයක් සිදුවිය: {e}")
            finally:
                # Cleanup temporary files
                if os.path.exists(pdf_path): os.remove(pdf_path)
                if os.path.exists(docx_path): os.remove(docx_path)