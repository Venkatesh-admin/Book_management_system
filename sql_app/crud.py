# book_management_system/sql_app/crud.py
import pickle
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sql_app import models, schemas
from sqlalchemy import func
from utils.security import get_password_hash, verify_password, create_access_token
from utils.llama3_summary import generate_summary
from fastapi import HTTPException
# Use the global model and dataframe
# Import model and data from ma
from load_model_data import load_model


async def create_user(db: AsyncSession, user):

    password=get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=password  # Hash the password before saving
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return {
            "message": "User created successfully",
            "user": db_user
            }
    except Exception as e:
        await db.rollback()
        return {
            "message": f"User creation failed: {str(e)}",
            "user": db_user
        }

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter_by(username=username))
    user = result.scalars().first()
    return user
async def get_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(models.User).filter_by(id=id))
    user = result.scalars().first()
    return user
async def get_user_by_email(db: AsyncSession, email:str):
    result = await db.execute(select(models.User).filter_by(email=email))
    user = result.scalars().first()
    return user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if user is None or not verify_password(password, user.password):
        return None
    return user

# Book CRUD Operations

async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        year_published=book.year_published,
        summary=generate_summary(book.content)
    )
    db.add(db_book)
    try:
        await db.commit()
        await db.refresh(db_book)
        return db_book
    except IntegrityError as e:
        await db.rollback()
        return None

async def get_all_books(db: AsyncSession):
    result = await db.execute(select(models.Book))
    books = result.scalars().all()
    return books

async def get_book_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(models.Book).filter_by(id=id))
    book = result.scalars().first()
    return book

async def update_book(db: AsyncSession, id: int, book: schemas.BookUpdate):
    result = await db.execute(select(models.Book).filter_by(id=id))
    db_book = result.scalars().first()
    if db_book:
        if book.title is not None:
            db_book.title = book.title
        if book.author is not None:
            db_book.author = book.author
        if book.genre is not None:
            db_book.genre = book.genre
        if book.year_published is not None:
            db_book.year_published = book.year_published
        if book.summary is not None:
            db_book.summary = generate_summary(book.summary)
        
        db.add(db_book)
        try:
            await db.commit()
            await db.refresh(db_book)
            return db_book
        except IntegrityError:
            await db.rollback()
            return None
    return None

async def delete_book(db: AsyncSession, id: int):
    result = await db.execute(select(models.Book).filter_by(id=id))
    db_book = result.scalars().first()
    if db_book:
        await db.delete(db_book)
        try:
            await db.commit()
            return True
        except IntegrityError:
            await db.rollback()
            return False
    return False

# Review CRUD Operations

async def add_review(db: AsyncSession, book_id: int, review: schemas.ReviewCreate):
    db_review = models.Review(
        book_id=book_id,
        user_id=review.user_id,
        review_text=review.review_text,
        rating=review.rating
    )
    db.add(db_review)
    try:
        await db.commit()
        await db.refresh(db_review)
        return db_review
    except IntegrityError:
        await db.rollback()
        return None

async def get_reviews_by_book_id(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Review).filter_by(book_id=book_id))
    reviews = result.scalars().all()
    return reviews

# Book Summary and Recommendations

async def get_book_summary(db: AsyncSession, id: int):
    result = await db.execute(select(models.Book).filter_by(id=id))
    book = result.scalars().first()
    if not book:
        return None
    
    # Aggregate reviews for summary
    review_result = await db.execute(select(func.avg(models.Review.rating).label('average_rating')).filter_by(book_id=id))
    
    average_rating = review_result.scalar()
    if average_rating is None:
        average_rating=0
    else:
        average_rating = round(average_rating,2)
    return {
        "summary": book.summary or "No summary available",
        "average_rating": average_rating
    }

async def recommend_books_by_preference(preferred_genres, num_recommendations=5):
    # Convert preferred genres to category codes
    model,df,label_encoder=load_model()
  
    
    try:
        preferred_codes = label_encoder.transform(preferred_genres)
    except ValueError as e:
        return {"error": "genre not present"}
    
    # Filter books by preferred genre codes
    filtered_df = df[df['genre_code'].isin(preferred_codes)]
    
    # Check if the filtered DataFrame is empty or too small
    if filtered_df.empty:
        return {"error": "No books found for the preferred genres"}
    
    # Ensure the number of recommendations does not exceed the number of available books
    num_recommendations = min(num_recommendations, len(filtered_df))
    
    X = filtered_df[['genre_code', 'average_rating']]
    
    # Use the model to find the nearest neighbors
    distances, indices = model.kneighbors(X, n_neighbors=num_recommendations)
    print(len(indices))
    # Flatten indices array if necessary
    indices = indices.flatten()
    
    # Ensure indices are within bounds
    valid_indices = [idx for idx in indices if 0 <= idx < len(filtered_df)]
    
    # Handle case where no valid indices are found
    if not valid_indices:
        return {"error": "No valid recommendations found"}
    
    # Get unique indices and sort them
    valid_indices = list(set(valid_indices))
    
    
    # Ensure indices are within bounds and fetch recommended books
    try:
        recommended_books = filtered_df.iloc[valid_indices]
        recommended_books = recommended_books.sort_values(by='average_rating', ascending=False).head(num_recommendations)
    except IndexError as e:
        return {"error": "Index out of bounds: " + str(e)}
    
    recommended_books= recommended_books[['id', 'title', 'author', 'genre', 'average_rating']]
    return {"books":recommended_books.to_dict(orient="records")}
