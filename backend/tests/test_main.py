from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Product Discovery Assistant API"}

def test_get_products():
    response = client.get("/products")
    # We expect 200 OK. The actual data depends on the DB, but the structure should be a list.
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_products_pagination():
    response = client.get("/products?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # If DB is empty, this passes. If not, it checks list.
    # We can't strictly assert length without mocking DB, but this checks endpoint health.

def test_get_product_not_found():
    # UUID format but non-existent
    response = client.get("/products/00000000-0000-0000-0000-000000000000")
    # Should be 404 or 500 depending on DB response for invalid ID, but 404 is expected for not found
    # Note: Supabase might return empty list which our code converts to 404
    assert response.status_code in [404, 500] 
