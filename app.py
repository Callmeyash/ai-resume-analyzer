import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

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
    
if st.button("Analyze Resume"):

        prompt = f"""
        Analyze this resume.

        Give:
        1. Resume Summary
        2. Top Skills
        3. Strengths
        4. Missing Skills
        5. Improvement Suggestions

        Resume:
        {text}
        """

        try:

            response = model.generate_content(
                prompt
            )

            st.subheader("AI Analysis")

            st.write(response.text)

        except Exception as e:

            st.error(f"Error: {e}")