import sys
sys.path.append("../external_ml")  # or use PYTHONPATH env var

# from notebooks import run_inference     # the external ML call

# async def process_image(data: bytes) -> dict:
#     result = run_inference(data)    # call it here
#     return {"label": result.label, "confidence": result.score}