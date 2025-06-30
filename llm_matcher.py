# llm_matcher.py
import subprocess

def get_match_score_llama(jd, resume_text):
    prompt = f"""
You are a resume screening assistant. Given a job description and a resume,
rate how well the resume matches the job on a scale of 1 to 10. Just return a number.

Job Description:
{jd}

Resume:
{resume_text}

Match Score (1-10):
"""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
