import streamlit as st
import pdfplumber
import os
import google.generativeai as genai

st.set_page_config(
    page_title="ResuAI",
    page_icon="📄",
    layout="centered" # Keeps everything tightly packed in the center column
)

# Premium UI CSS Injection
st.markdown("""
    <style>
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Center the branding header */
    .hero-container {
        text-align: center;
        padding-top: 50px;
        padding-bottom: 20px;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #FFFFFF;
        margin-bottom: 0px;
    }
    .hero-tagline {
        font-size: 18px;
        color: #64748B;
        margin-top: 5px;
        margin-bottom: 40px;
    }
    
    /* Clean glassmorphic styling for files */
    .uploadedFile {
        border: 1px dashed #334155 !important;
        background-color: #0F172A !important;
        border-radius: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Clean Header Zone
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">ResuAI</h1>
        <p class="hero-tagline">How can we optimize your professional profile today?</p>
    </div>
""", unsafe_allow_html=True)

# Centered file upload zone
uploaded_files = st.file_uploader("Drop resume PDF here", type=["pdf"], label_visibility="collapsed")

resume_text = ""
if uploaded_files:
    st.toast("Document uploaded!", icon="✅") # Slick, non-intrusive toast notification
    with pdfplumber.open(uploaded_files) as pdf:
        resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

st.markdown("<br>", unsafe_allow_html=True)

# Implementing the Suggestion Grid Layout 
st.markdown("<p style='text-align: center; color: #94A3B8; font-weight: 500;'>Select Target Profile</p>", unsafe_allow_html=True)

# This creates a clickable grid of quick-options just like your classmate's site
col1, col2 = st.columns(2)
selected_role = ""

with col1:
    if st.button("🤖 AI / Machine Learning Engineer", use_container_width=True):
        selected_role = "AI / Machine Learning Engineer"
    if st.button("💻 Full Stack Developer", use_container_width=True):
        selected_role = "Full Stack Developer"

with col2:
    if st.button("📊 Data Scientist", use_container_width=True):
        selected_role = "Data Scientist"
    if st.button("🛡️ Cyber Security Analyst", use_container_width=True):
        selected_role = "Cyber Security Analyst"

# Custom text input field if their role isn't in the quick grid
custom_role = st.text_input("", placeholder="Or type a custom target role here...", label_visibility="collapsed")

# Resolve which role to use
final_job_role = custom_role if custom_role else selected_role

# Display active target selection badge
if final_job_role:
    st.markdown(f"<div style='text-align: center; margin-top: 15px;'><span style='background-color: #1E293B; color: #38BDF8; padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 600;'>Targeting: {final_job_role}</span></div>", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #1E293B;'><br>", unsafe_allow_html=True)

# Trigger Button
if st.button("Run ATS Analysis Engine", type="primary", use_container_width=True):
    if not uploaded_files:
        st.error("Please drop a resume PDF file first.")
    elif not final_job_role:
        st.error("Please select or enter a target role.")
    else:
        with st.spinner("Processing deep optimization check..."):
            # Put your model logic here
            st.success("Analysis complete!")
