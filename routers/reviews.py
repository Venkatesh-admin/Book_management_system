# book_management_system/routers/reviews.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sql_app import crud, schemas
from sql_app.database import get_db
from utils.security import get_current_user
router = APIRouter()

@router.post("/books/{id}/reviews", response_model=schemas.ReviewAddResponse)
async def add_review(id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):#
    result = await crud.add_review(db, id, review)
    if result:
        return {"message": "Review added successfully", "data": result}
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/books/{id}/reviews", response_model=schemas.ReviewListResponse)
async def get_reviews(id: int, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):#, user = Depends(get_current_user)
    reviews = await crud.get_reviews_by_book_id(db, id)
    if reviews:
        return {"reviews":reviews}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
