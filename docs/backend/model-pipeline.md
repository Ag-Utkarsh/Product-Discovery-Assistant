# Model Pipeline (RAG)

The core intelligence of the Product Discovery Assistant relies on a Retrieval-Augmented Generation (RAG) pipeline. This allows the system to ground its answers in the actual product data stored in Supabase.

## Pipeline Steps

### 1. Query Expansion (LLM)
*   **Input:** User's raw natural language query (e.g., "something to sit on for a balcony").
*   **Process:** An LLM (Google Gemini) analyzes the intent and generates a list of optimized search terms.
*   **Output:** Expanded keywords (e.g., "outdoor chair, balcony seating, patio furniture, weather-resistant chair").
*   **Why?** This bridges the gap between how users talk and how products are indexed.

### 2. Vector Search (Supabase pgvector)
*   **Input:** Expanded search terms.
*   **Process:**
    1.  The search terms are converted into a high-dimensional vector using an Embedding Model (e.g., `text-embedding-004`).
    2.  This vector is compared against the pre-computed vectors of all products in the database using Cosine Similarity.
*   **Output:** A ranked list of the most semantically similar products.

### 3. Synthesis (LLM)
*   **Input:** The user's original query + The list of retrieved products (JSON data).
*   **Process:** The LLM acts as a sales assistant. It reviews the retrieved products and generates a helpful response that explains *why* these specific items were recommended.
*   **Output:** A natural language response (e.g., "I found these great outdoor chairs that are perfect for compact balconies...").

## Configuration

The pipeline is configured in `app/services/llm.py` and `app/services/rag.py`.

*   **Embedding Model:** `text-embedding-004` (768 dimensions).
*   **Chat Model:** `gemini-2.5-flash`.
*   **Similarity Threshold:** Configurable in `rag.py` (default: 0.5) to filter out irrelevant matches.
