from fastapi import APIRouter
from app.core.distance import haversine
from app.core.similarity import compute_cosine_similarity

router = APIRouter(prefix="/calculate", tags=["Calculation Algorithms"])

@router.post("/haversine")
async def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    result = await haversine(lat1, lon1, lat2, lon2)
    return result

@router.post("/cosine-similarity")
async def cosine_similarity(tutor_description: str, student_description: str):
    result = await compute_cosine_similarity(tutor_description, student_description)
    return result

