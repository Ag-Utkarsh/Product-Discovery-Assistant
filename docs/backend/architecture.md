# Backend Architecture

## Overview

The backend of the Product Discovery Assistant is built using **FastAPI**, designed to be high-performance and easy to extend. It serves as the bridge between the frontend, the database (Supabase), and the AI models (Google Gemini).

## Data Flow

1.  **Request Handling (API):**
    *   The Frontend sends HTTP requests to the FastAPI endpoints.
    *   **Product Listing:** Fetches paginated data directly from Supabase.
    *   **Chat/Search:** Sends the user query to the RAG pipeline.

2.  **RAG Pipeline (Search & Inference):**
    *   **Query Expansion:** The user's raw query is expanded by an LLM to include synonyms and related terms (e.g., "small bed" -> "compact, single, space-saving").
    *   **Vector Search:** The expanded query is converted to an embedding vector. This vector is compared against stored product embeddings in Supabase using `pgvector` (cosine similarity).
    *   **Synthesis:** The top matching products are retrieved and passed to the LLM along with the original query. The LLM generates a natural language response explaining *why* these products match.

## Tech Stack

*   **Framework:** FastAPI (Python)
*   **Database:** Supabase (PostgreSQL)
*   **Vector Store:** pgvector (within Supabase)
*   **AI/LLM:** Google Gemini 2.5 Flash
*   **Server:** Uvicorn (ASGI)

## Key Components

*   `app/main.py`: Entry point, defines API routes and middleware (CORS, Rate Limiting).
*   `app/services/product_service.py`: Handles database interactions for standard CRUD operations.
*   `app/services/rag.py`: Manages the retrieval logic (embedding generation + vector search).
*   `app/services/llm.py`: Interfaces with the LLM provider for query expansion and response synthesis.
