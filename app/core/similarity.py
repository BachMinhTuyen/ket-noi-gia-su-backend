from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

async def compute_cosine_similarity(tutor_description, student_description):
    
    sentences = [tutor_description, student_description]
    model = SentenceTransformer("distiluse-base-multilingual-cased-v2")
    
    embeddings = model.encode(sentences)
    
    similarity = cosine_similarity(
                [embeddings[0]], 
                [embeddings[1]]
            )[0][0]
    
    return float(np.clip(similarity, 0.0, 1.0))

# tutor_description = "Tôi có kinh nghiệm giảng dạy toán, lý, hóa."
# student_description = "Tôi muốn tìm gia sư môn toán."
