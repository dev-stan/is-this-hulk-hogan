from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas import AnalysisResult

router = APIRouter()

@router.post("/compare_images", response_model=AnalysisResult)
async def compare_images(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(400, "Unsupported image type")
    
    return await "Returning data..."