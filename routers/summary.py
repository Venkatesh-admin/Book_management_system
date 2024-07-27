# book_management_system/routers/summary.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sql_app import crud, schemas
from sql_app.database import get_db
from utils.llama3_summary import generate_summary  # Import your summary generation function
from sql_app.schemas import GenerateSummaryRequest
from utils.security import get_current_user
from fastapi import APIRouter, Depends
router = APIRouter()

@router.post("/generate-summary")
async def generate_summary_endpoint(request: GenerateSummaryRequest,user = Depends(get_current_user)):
    try:
        summary = generate_summary(request.content)  # Use your AI model here
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
