# API Specification

Base URL: `http://localhost:8000` (Local)

## Endpoints

### 1. Health Check
*   **URL:** `/`
*   **Method:** `GET`
*   **Description:** Verifies that the API is running.
*   **Response:**
    ```json
    {
      "message": "Welcome to Product Discovery Assistant API"
    }
    ```

### 2. List Products
*   **URL:** `/products`
*   **Method:** `GET`
*   **Description:** Retrieves a paginated list of products.
*   **Query Parameters:**
    *   `limit` (int, default=20): Number of items to return.
    *   `offset` (int, default=0): Number of items to skip.
*   **Response:** `List[Product]`
    ```json
    [
      {
        "id": "uuid",
        "title": "Product Name",
        "price": 1000,
        "image_url": "http://...",
        ...
      }
    ]
    ```

### 3. Get Product Details
*   **URL:** `/products/{product_id}`
*   **Method:** `GET`
*   **Description:** Retrieves details for a specific product.
*   **Path Parameters:**
    *   `product_id` (str): UUID of the product.
*   **Response:** `Product` object.

### 4. Chat (RAG Search)
*   **URL:** `/chat`
*   **Method:** `POST`
*   **Description:** Processes a natural language query and returns an AI-generated response with product recommendations.
*   **Payload:**
    ```json
    {
      "query": "I need a bed for a small room"
    }
    ```
*   **Response:**
    ```json
    {
      "response": "Based on your needs, I recommend the Single Bed...",
      "products": [ ... ] // List of recommended Product objects
    }
    ```

## Data Models

### Product
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Unique identifier |
| `sku_id` | String | Source system ID |
| `title` | String | Product name |
| `price` | Integer | Price in currency units |
| `description` | String | Product description |
| `image_url` | String | URL to product image |
| `features` | JSON | Key-value pairs of features |
