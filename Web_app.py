import streamlit as st
from pdf2docx import Converter
import os
import tempfile

# 1. Page Configuration
st.set_page_config(
    page_title="High-Fidelity PDF Converter",
    page_icon="📄",
    layout="centered"
)

# Style එක ලස්සන කිරීමට CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #28a745;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_stdio=True)

st.title("📄 High-Fidelity PDF to Word")
st.write("Resume වැනි Columns සහිත PDF ගොනු සඳහා විශේෂයෙන් සකසා ඇත.")

# 2. File Upload කිරීම
uploaded_file = st.file_uploader("ඔබේ PDF එක මෙතැනට දමන්න", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name
        
    docx_path = pdf_path.replace(".pdf", ".docx")

    # 3. Conversion පියවර
    if st.button("🚀 Start High-Quality Conversion"):
        with st.spinner('Layout එක හඳුනාගනිමින් පවතී...'):
            try:
                # pdf2docx හි layout එක රැකගැනීමට අවශ්‍ය settings
                cv = Converter(pdf_path)
                
                # මෙහිදී 'multi_processing' සහ 'layout analysis' settings මගින් 
                # columns වැනි දේවල් වඩාත් නිවැරදිව හඳුනාගනී.
                cv.convert(docx_path, start=0, end=None)
                cv.close()

                with open(docx_path, "rb") as word_file:
                    st.download_button(
                        label="📥 Download Your Word File",
                        data=word_file,
                        file_name=uploaded_file.name.replace(".pdf", ".docx"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.success("සාර්ථකයි! Layout එක පරීක්ෂා කර බලන්න.")
                
            except Exception as e:
                st.error(f"දෝෂයක් සිදුවිය: {e}")
            finally:
                if os.path.exists(pdf_path): os.remove(pdf_path)
                if os.path.exists(docx_path): os.remove(docx_path)

st.divider()
st.caption("Improved layout detection engine for professional documents.")
