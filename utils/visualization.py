import streamlit as st
import difflib

def create_comparison_view(analysis_results: dict):
    """Create a side-by-side comparison view with highlighting."""
    st.markdown("""
    <style>
    .highlight-match {
        background-color: #90EE90;
        padding: 2px 4px;
        border-radius: 3px;
    }
    .highlight-missing {
        background-color: #FFB6C6;
        padding: 2px 4px;
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

    def highlight_text(text, keywords, missing_keywords):
        """Highlight matching and missing keywords in text."""
        for keyword in keywords:
            text = text.replace(keyword, f'<span class="highlight-match">{keyword}</span>')
        for keyword in missing_keywords:
            text = text.replace(keyword, f'<span class="highlight-missing">{keyword}</span>')
        return text

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Your Resume")
        highlighted_resume = highlight_text(
            "Sample resume text...",  # In real implementation, this would be the actual resume text
            analysis_results['matched_keywords'],
            []
        )
        st.markdown(highlighted_resume, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Job Description")
        highlighted_job = highlight_text(
            "Sample job description...",  # In real implementation, this would be the actual job description
            analysis_results['matched_keywords'],
            analysis_results['missing_keywords']
        )
        st.markdown(highlighted_job, unsafe_allow_html=True)
