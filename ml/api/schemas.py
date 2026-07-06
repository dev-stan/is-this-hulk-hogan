from pydantic import BaseModel

class AnalysisResult(BaseModel):
    label: str
    confidence: float