# tests/test_main.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_user_registration():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

@pytest.mark.asyncio
async def test_user_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

@pytest.mark.asyncio
async def test_add_book():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/books/", json={"title": "Test Book", "author": "Test Author", "genre": "Fiction", "year_published": 2020}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"

@pytest.mark.asyncio
async def test_get_books():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_book_by_id():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

@pytest.mark.asyncio
async def test_update_book():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/books/1", json={"title": "Updated Book", "author": "Updated Author", "genre": "Non-Fiction", "year_published": 2021}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Book updated successfully"

@pytest.mark.asyncio
async def test_delete_book():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/books/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

@pytest.mark.asyncio
async def test_add_review():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/books/1/reviews", json={"user_id": 1, "review_text": "Great book!", "rating": 5}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Review added successfully"

@pytest.mark.asyncio
async def test_get_reviews():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/1/reviews", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_summary():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/1/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "summary" in response.json()

@pytest.mark.asyncio
async def test_get_recommendations():
    token = await test_user_login()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/recommendations", json={"genres": ["Fiction"]}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()["books"]) > 0
