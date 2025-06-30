import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf
from llm_matcher import get_match_score_llama

# Page setup
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("📄 AI-Powered Resume Screener")

# Input for Job Description
jd = st.text_area("📝 Paste the Job Description", height=200)

# Upload resume PDFs
uploaded_files = st.file_uploader("📂 Upload Resume PDFs", type="pdf", accept_multiple_files=True)

# Button to start screening
if st.button("🚀 Screen Resumes"):
    if not jd:
        st.warning("⚠️ Please paste a job description first.")
    elif not uploaded_files:
        st.warning("⚠️ Please upload at least one resume.")
    else:
        st.info("🔍 Screening in progress... please wait...")

        results = []

        for uploaded_file in uploaded_files:
            try:
                # Extract resume text
                resume_text = extract_text_from_pdf(uploaded_file)

                # Get match score from LLaMA
                score = get_match_score_llama(jd, resume_text)

                results.append({
                    "Filename": uploaded_file.name,
                    "Match Score": score
                })
            except Exception as e:
                results.append({
                    "Filename": uploaded_file.name,
                    "Match Score": f"❌ Error: {str(e)}"
                })

        # Create DataFrame and sort
        df = pd.DataFrame(results)

        try:
            df["Match Score"] = pd.to_numeric(df["Match Score"], errors='coerce')
            df = df.sort_values(by="Match Score", ascending=False)
        except:
            pass  # In case some scores are invalid

        # Show results
        st.success("✅ Screening Complete!")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Ranked Resumes CSV",
            data=csv,
            file_name="ranked_resumes.csv",
            mime="text/csv"
        )
