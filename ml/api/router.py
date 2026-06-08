from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas import AnalysisResult
from service import process_image

router = APIRouter()

@router.post("/compare_images", response_model=AnalysisResult)
async def compare_images(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(400, "Unsupported image type")
    
    data = await file.read()
    return await process_image(data)