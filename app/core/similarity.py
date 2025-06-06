from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Optional
from app.models import Subject
# import os
# model = SentenceTransformer("distiluse-base-multilingual-cased-v2")  # Hỗ trợ tiếng Việt
model = SentenceTransformer("app/core/output/subject-matching-model") # Mô hình đã training

# print(os.path.exists("output/subject-matching-model"))
# print(os.listdir("app/core/output/subject-matching-model"))

async def compute_cosine_similarity(tutor_description, student_description):
    
    sentences = [tutor_description, student_description]
    
    embeddings = model.encode(sentences)
    
    similarity = cosine_similarity(
                [embeddings[0]], 
                [embeddings[1]]
            )[0][0]
    
    return float(np.clip(similarity, 0.0, 1.0))

# tutor_description = "Tôi có kinh nghiệm giảng dạy toán, lý, hóa."
# student_description = "Tôi muốn tìm gia sư môn toán."


async def find_matching_subject(keyword: str, subjects: list) -> Optional[Subject]:
    keyword_embedding = model.encode([keyword])[0]
    
    best_score = 0.0
    best_subject = None

    for subj in subjects:
        subject_text = f"{subj.subjectName_vi}"
        subject_lower_text = subject_text.lower()
        subj_embedding = model.encode([subject_lower_text])[0]
        score = cosine_similarity([keyword_embedding], [subj_embedding])[0][0]
        
        if score > best_score:
            best_score = score
            best_subject = subj
    print('-------------------------'   )
    print(f"{best_subject.subjectName_vi} - {best_score}")
    print('-------------------------')
    if best_score >= 0.6:
        return best_subject
    return None
