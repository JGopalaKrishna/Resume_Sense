from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(resume_vectors, jd_vector):
    scores=[]
    for one_resume_token in resume_vectors:
        matched_keywords = jd_vector.intersection(one_resume_token)
        if len(jd_vector) == 0:
            scores.append(0)
        else:
            score=round( (len(matched_keywords) / len(jd_vector))*100,2)
            scores.append(score)
    return scores