# book_management_system/routers/books.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sql_app import crud, schemas
from sql_app.database import get_db
from utils.security import get_current_user
from typing import List
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post("/books/")
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    result= await crud.create_book(db, book)
    result = schemas.BookResponse(author=result.author,
                                  message="Book added Successfully",
                                  id=result.id,
                                  year_published=result.year_published,
                                  summary=result.summary,
                                  genre=result.genre,title=result.title)
    return result

@router.get("/books/", response_model=schemas.BookListResponse)
async def get_books(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    result =await crud.get_all_books(db)
    if result:
        return {"books":result}
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/books/{id}", response_model=schemas.BookResponse)
async def get_book(id: int, db: AsyncSession = Depends(get_db), user= Depends(get_current_user)):
    result = await crud.get_book_by_id(db, id)
    if result:
        result=schemas.BookResponse(author=result.author,
                                  message="Book updated Successfully",
                                  id=result.id,
                                  year_published=result.year_published,
                                  summary=result.summary,
                                  genre=result.genre,title=result.title)
        return result
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    

@router.put("/books/{id}", response_model=schemas.BookResponse)
async def update_book(id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db), user= Depends(get_current_user)):
    result = await crud.update_book(db, id, book)
    if result:
        result=schemas.BookResponse(author=result.author,
                                  message="Book updated Successfully",
                                  id=result.id,
                                  year_published=result.year_published,
                                  summary=result.summary,
                                  genre=result.genre,
                                  title=result.title)
        return result
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/books/{id}")
async def delete_book(id: int, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    deleted = await crud.delete_book(db, id)
    if deleted:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/books/{id}/summary", response_model=schemas.BookSummaryResponse)
async def get_book_summary(id: int, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    summary = await crud.get_book_summary(db, id)
    if summary:
        return summary
    else:
        raise HTTPException(status_code=404, detail="Book not found")





@router.post("/recommendataions/")
async def get_recommendations_by_preference(recommenations:schemas.RecommendationsRequest,user = Depends(get_current_user)):#
    return await crud.recommend_books_by_preference(recommenations.genres, num_recommendations=5)
    r
    
