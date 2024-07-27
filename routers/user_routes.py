# book_management_system/routers/user_routes.py

from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sql_app import crud, schemas
from sql_app.database import get_db
from utils.security import verify_password,create_access_token

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
async def create_user(user:schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result1=await crud.get_user_by_username(db,user.username)
    if result1:
        return {"message":"User already exists with username","user":None}
    result2=await crud.get_user_by_email(db,user.email)
    if result2:
        return {"message":"User already exists with username","user":None}
    return await crud.create_user(db, user)
    

@router.post("/login", response_model=schemas.LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "message": "User logged in successfully"}