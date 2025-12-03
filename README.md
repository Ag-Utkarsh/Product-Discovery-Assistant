# Product Discovery Assistant

> **Status:** Beta 🚀

The **Product Discovery Assistant** is an end-to-end RAG (Retrieval-Augmented Generation) e-commerce assistant designed to transform how users find products. Unlike traditional keyword search, it understands abstract natural language queries (e.g., "bed for a small room") and provides intelligent, context-aware product recommendations with visual cards.

## ✨ Features

-   **AI-Powered Search:** Uses LLMs to "reason" about user queries and translate them into effective database searches.
-   **RAG Pipeline:** Combines vector search (Supabase pgvector) with LLM synthesis for accurate and explained results.
-   **Visual Recommendations:** Returns rich product cards with images, prices, and details, not just text.
-   **Modern Stack:** Built with React (Vite) for a responsive frontend and FastAPI for a high-performance backend.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

-   **Node.js** (v18 or higher)
-   **Python** (v3.10 or higher)
-   **Git**
-   **Supabase Account** (for Database & Vector Search)
-   **Google Gemini API Key** (for LLM & Embeddings)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd product-discovery-assistant
```

### 2. Backend Setup

Navigate to the backend directory and set up the Python environment.

```bash
cd backend
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirement.txt
```

**Environment Configuration:**
Create a `.env` file in the `backend` directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GOOGLE_API_KEY=your_google_api_key
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies.

```bash
cd ../frontend
npm install
```

**Environment Configuration:**
Create a `.env` file in the `frontend` directory (optional if using default localhost):

```env
VITE_API_URL=http://localhost:8000
```

## 🏃 Usage

### Start the Backend Server

From the `backend` directory (with venv activated):

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Documentation: `http://localhost:8000/docs`

### Start the Frontend Server

From the `frontend` directory:

```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

## 🧪 Testing

### Backend
Run unit tests using pytest:

```bash
cd backend
pytest
```

### Frontend
Run linting to check for code quality issues:

```bash
cd frontend
npm run lint

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.
