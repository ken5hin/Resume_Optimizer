import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.document_parser import parse_document
from utils.text_analyzer import analyze_text, calculate_ats_score
from utils.visualization import create_comparison_view
import base64

st.set_page_config(
    page_title="Resume ATS Optimizer",
    page_icon="📄",
    layout="wide"
)

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    
    st.title("📄 Resume ATS Optimizer")
    st.markdown("""
    Optimize your resume for Applicant Tracking Systems (ATS) and increase your chances of getting noticed!
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload Resume")
        resume_file = st.file_uploader("Choose your resume (PDF/DOCX)", type=["pdf", "docx"])

    with col2:
        st.subheader("Job Description")
        job_description = st.text_area("Paste the job description here", height=200)

    if resume_file and job_description:
        with st.spinner("Analyzing your resume..."):
            # Parse resume
            resume_text = parse_document(resume_file)

            # Analyze texts
            analysis_results = analyze_text(resume_text, job_description)
            ats_score = calculate_ats_score(analysis_results)

            # Display results
            st.header("Analysis Results")

            # Score display
            score_col, chart_col = st.columns([1, 2])
            with score_col:
                st.metric("ATS Score", f"{ats_score}%")
                if ats_score >= 90:
                    st.success("Great! Your resume is well-optimized for this position!")
                else:
                    st.warning("Your resume could use some optimization.")

            with chart_col:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=ats_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#0066cc"},
                           'steps': [
                               {'range': [0, 60], 'color': "#ff4b4b"},
                               {'range': [60, 80], 'color': "#ffa500"},
                               {'range': [80, 100], 'color': "#00cc66"}
                           ]}))
                fig.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)

            # Comparison view
            st.subheader("Resume vs Job Description Comparison")
            create_comparison_view(analysis_results)

            # Recommendations
            st.subheader("Recommendations")
            for category, recommendations in analysis_results['recommendations'].items():
                with st.expander(f"{category} Recommendations"):
                    for rec in recommendations:
                        st.markdown(f"- {rec}")

            # Keywords
            st.subheader("Important Keywords")
            missing_keywords = analysis_results['missing_keywords']
            matched_keywords = analysis_results['matched_keywords']
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ✅ Matched Keywords")
                st.write(", ".join(matched_keywords))
            with col2:
                st.markdown("#### ❌ Missing Keywords")
                st.write(", ".join(missing_keywords))

if __name__ == "__main__":
    main()
