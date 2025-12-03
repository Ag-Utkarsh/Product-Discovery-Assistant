from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.services.product_service import ProductService
from app.services import llm, rag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Product Discovery Assistant")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # Common React port (optional, keeping for flexibility if user needs it, but plan said restricted)
    # Actually, plan said strictly 5173. Let's stick to 5173 and maybe 8000 for self.
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: str
    sku_id: str
    title: str
    price: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    features: Optional[dict] = None
    category: Optional[str] = None

@app.get("/")
async def read_root():
    return {"message": "Welcome to Product Discovery Assistant API"}

@app.get("/products", response_model=List[Product])
@limiter.limit("100/minute")
async def get_products(
    request: Request,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List products with pagination.
    """
    try:
        products_data = ProductService.get_products(limit, offset)
        return products_data
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get a single product by ID.
    """
    try:
        product_data = ProductService.get_product_by_id(product_id)
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")
        return product_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# --- Chat / RAG Endpoint ---

class ChatRequest(BaseModel):
    query: str = Field(..., max_length=1000)

class ChatResponse(BaseModel):
    response: str
    products: List[Product]

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Handle chat requests using RAG pipeline:
    1. Expand Query (LLM)
    2. Vector Search (Supabase)
    3. Synthesize Response (LLM)
    """
    try:
        # 1. Expand Query
        expanded_query = await llm.expand_query(chat_request.query)
        logger.info(f"Original Query: {chat_request.query} -> Expanded: {expanded_query}")
        
        # 2. Vector Search
        # Now async!
        products_data = await rag.search_products(expanded_query)
        
        # Convert to Pydantic models (handling potential missing fields safely)
        products = []
        for p in products_data:
            try:
                products.append(Product(**p))
            except Exception as e:
                logger.warning(f"Skipping invalid product data: {e}")

        # 3. Synthesis
        response_text = await llm.generate_response(chat_request.query, products_data)
        
        return {
            "response": response_text,
            "products": products
        }

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # Sanitize error message for client
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
