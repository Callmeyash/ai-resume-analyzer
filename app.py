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

with st.sidebar:
    st.header("AI Resume Analyzer")
    st.write("Upload a PDF resume and receive AI-powered feedback.")

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
job_role = st.text_input("Enter Target Role")
with st.spinner("Analyzing Resume..."):
    if st.button("Analyze Resume"):

        prompt = f"""
        Analyze this resume for the role: {job_role}

        Provide:
        1. Resume Summary
        2. Matching Skills
        3. Missing Skills
        4. Skill Gap Analysis
        5. Projects Needed
        6. ATS Score
        7. Resume Score (0-10)

        Resume:
        {text}
        """

        try:

            response = model.generate_content(
                prompt
            )

            st.subheader("AI Analysis")

            st.markdown(response.text)
            st.success("Analysis Complete!")
            st.download_button(
            "Download Analysis",
            response.text,
            file_name="resume_analysis.txt"
)

        except Exception as e:

            st.error(f"Error: {e}")

