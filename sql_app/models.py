# book_management_system/sql_app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sql_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String, index=True)
    year_published = Column(Integer)
    summary = Column(Text, nullable=True)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE",onupdate="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE",onupdate="CASCADE"))
    review_text = Column(Text)
    rating = Column(Float)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
