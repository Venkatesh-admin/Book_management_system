# book_management_system/sql_app/schemas.py

from pydantic import BaseModel,EmailStr
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    message:str
    user:Optional[UserPublic]=None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    content: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None



class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None
    message:Optional[str]=None

class BookListResponse(BaseModel):
    books: List[BookUpdate]

class ReviewCreate(BaseModel):
    user_id: int
    review_text: str
    rating: int

class ReviewResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    review_text: str
    rating: int

    class Config:
        orm_mode = True

class ReviewAddResponse(BaseModel):
    data:ReviewResponse
    message:str

class ReviewListResponse(BaseModel):
    reviews: List[ReviewResponse]

class BookSummaryResponse(BaseModel):
    summary: str
    average_rating: float

class BookContent(BaseModel):
    content: str

class SummaryResponse(BaseModel):
    summary: str

class GenerateSummaryRequest(BaseModel):
    content: str


class RecommendationsRequest(BaseModel):
    genres: List[str]