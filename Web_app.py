import streamlit as st
from pdf2docx import Converter
import os
import tempfile

# 1. Page Configuration - පෙනුම සැකසීම
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
        border-radius: 12px;
        height: 3.5em;
        background-color: #28a745;
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #218838;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 High-Fidelity PDF to Word")
st.write("Resume වැනි Columns සහ Tables සහිත PDF ගොනු නිවැරදිව Word බවට පත් කිරීමට මෙය භාවිතා කරන්න.")

# 2. File Upload කිරීම
uploaded_file = st.file_uploader("ඔබේ PDF එක මෙතැනට දමන්න (Upload PDF)", type="pdf")

if uploaded_file is not None:
    # තාවකාලිකව පරිගණකයේ PDF එක තබා ගැනීම
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name
        
    docx_path = pdf_path.replace(".pdf", ".docx")

    # 3. Conversion පියවර
    if st.button("🚀 Start High-Quality Conversion"):
        with st.spinner('Layout එක සහ අකුරු හඳුනාගනිමින් පවතී...'):
            try:
                # pdf2docx හි layout එක රැකගැනීමට අවශ්‍ය Settings
                cv = Converter(pdf_path)
                
                # මෙහිදී 'multi_processing' සහ 'layout analysis' හරහා 
                # Resume එකක තියෙන columns (දෙපැත්තට බෙදීම) වඩාත් හොඳින් හඳුනාගනී.
                cv.convert(docx_path, start=0, end=None)
                cv.close()

                # 4. Download Button එක පෙන්වීම
                with open(docx_path, "rb") as word_file:
                    st.download_button(
                        label="📥 Download Converted Word File",
                        data=word_file,
                        file_name=uploaded_file.name.replace(".pdf", ".docx"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.success("සාර්ථකයි! දැන් ඔබේ Word File එක බාගත කරගන්න.")
                
            except Exception as e:
                st.error(f"දෝෂයක් සිදුවිය: {e}")
            finally:
                # වැඩේ ඉවර වුණාම තාවකාලික files මකා දැමීම
                if os.path.exists(pdf_path): os.remove(pdf_path)
                if os.path.exists(docx_path): os.remove(docx_path)

st.divider()
st.caption("Optimized for Professional Resumes and Multi-column Layouts.")
