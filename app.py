import streamlit as st
import pdfplumber

st.title("AI Resume Analyzer")
st.write("Upload your resume for analysis")

uploaded_files = st.file_uploader(
    "Upload Resume ⬇️",
    type=["pdf"]
)

if uploaded_files: 
    st.success("Resume Uploaded Successfully")

    with pdfplumber.open(uploaded_files)as pdf:
        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text+= page_text + "\n"
    
    st.subheader("Extracted Resume Text")

    st.text(text[:5000])
    