import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="ResuAI | Advanced Resume Analyzer",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Modern CSS Injection for a sleek tech-SaaS look
st.markdown("""
    <style>
    /* Gradient Main Title */
    .main-title {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(90deg, #2563EB, #38BDF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 35px;
    }
    /* Sleek container styles for files and parameters */
    .css-1r6g72q, .stFieldSet {
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Environment Variables & Initialize Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("Missing GEMINI_API_KEY. Please set it in your .env file or Streamlit Secrets.")

if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")

# 4. Sidebar Branding
with st.sidebar:
    st.markdown("## 📄 ResuAI Pro")
    st.markdown("---")
    st.markdown("⚡ **Powered by Gemini 2.5 Flash**")
    st.write("This intelligence engine parses your professional experience, matches it against target market rules, and instantly surfaces gaps and optimizations.")
    st.markdown("---")
    st.caption("v1.2.0 • Secured Data Sandbox")

# 5. Main Dashboard Header
st.markdown('<h1 class="main-title">AI Resume Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Optimize your professional profile for ATS algorithms instantly</p>', unsafe_allow_html=True)

# 6. User Inputs Area
uploaded_files = st.file_uploader(
    "Upload your resume (PDF format)",
    type=["pdf"],
    label_visibility="collapsed"
)

# Text extraction logic executed dynamically if a file exists
resume_text = ""
if uploaded_files: 
    st.success("✅ Document uploaded and parsed successfully.")
    
    with pdfplumber.open(uploaded_files) as pdf:
        text_list = []
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_list.append(page_text)
        resume_text = "\n".join(text_list)
    
    # Expandable preview box so it stays organized and doesn't take up 5 miles of scrolling
    with st.expander("🔍 View Extracted Text Preview"):
        st.text_area("Parsed Raw Content", value=resume_text[:3000], height=200, disabled=True)

st.markdown("### Target Profile Details")
job_role = st.text_input("Enter Target Role:", placeholder="e.g., Software Engineer, Data Scientist, AI Engineer")

st.markdown("---")

# 7. Execution and Trigger Logic (Fixed structured condition blocks)
if st.button("Analyze Resume", type="primary", use_container_width=True):
    if not uploaded_files:
        st.warning("Please upload a resume file first.")
    elif not job_role.strip():
        st.warning("Please specify a Target Role to optimize against.")
    else:
        # Modern multi-step progress indicator box instead of simple spinner text
        with st.status("Analyzing your application profile...", expanded=True) as status:
            st.write("Running token compliance metrics...")
            
            prompt = f"""
            Analyze this resume for the role: {job_role}

            Provide your response in beautifully formatted markdown with bold highlights, clear structural titles, and lists. Include:
            1. **Resume Summary** (2-3 concise sentences)
            2. **Matching Skills** (Bullet list)
            3. **Missing Skills** (Bullet list)
            4. **Skill Gap Analysis**
            5. **Projects Needed** (Concrete project ideas to build to close gaps)
            6. **ATS Score** (Percentage matching layout estimation)
            7. **Resume Score** (0-10 Scale rating)

            Resume Text Content:
            {resume_text}
            """
            
            try:
                st.write("Parsing structural patterns against industry expectations...")
                response = model.generate_content(prompt)
                
                status.update(label="Analysis Finished!", state="complete", expanded=False)
                
                # Render results down in clear, responsive layouts
                st.markdown("## 📊 AI Evaluation Insights")
                st.markdown(response.text)
                
                st.markdown("---")
                
                # Secondary action download button
                st.download_button(
                    label="💾 Download Raw Analysis Report",
                    data=response.text,
                    file_name=f"{job_role.lower().replace(' ', '_')}_analysis.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:
                status.update(label="An error occurred", state="error")
                st.error(f"Execution Error details: {e}")
