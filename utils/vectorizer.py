from sklearn.feature_extraction.text import TfidfVectorizer
import re

def vectorize_texts(resumes, job_description):

    def preprocess(text):
        tokens = re.findall(r'\b[a-zA-Z0-9\.-]+\b', text.lower())
        return set(tokens)

    jd_tokens = preprocess(job_description)
    all_resume_tokens=[]

    for one_resume in resumes:
        resume_token = preprocess(one_resume)
        all_resume_tokens.append(resume_token)

    return all_resume_tokens,jd_tokens
