import google.generativeai as genai
from app.core.config import GOOGLE_API_KEY
from app.core.db import supabase
from fastapi.concurrency import run_in_threadpool
import logging

logger = logging.getLogger(__name__)

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set in .env file")

genai.configure(api_key=GOOGLE_API_KEY)

async def search_products(query: str, match_threshold: float = 0.5, match_count: int = 5):
    """
    Searches for products using vector similarity.
    """
    # For query embedding, we use task_type="retrieval_query"
    try:
        # genai.embed_content_async is not standard, using run_in_threadpool for safety if async not available
        # But actually, let's use the sync method in threadpool to be safe and consistent
        result = await run_in_threadpool(
            genai.embed_content,
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )
        query_embedding = result['embedding']
    except Exception as e:
        logger.error(f"Error generating query embedding: {e}")
        return []

    if not query_embedding:
        return []
    
    try:
        # 1. Get similar product IDs from vector search (Supabase RPC is sync)
        response = await run_in_threadpool(
            lambda: supabase.rpc(
                'match_products',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': match_threshold,
                    'match_count': match_count
                }
            ).execute()
        )
        
        matches = response.data
        if not matches:
            return []
            
        # 2. Extract Product IDs
        product_ids = [match['product_id'] for match in matches]
        
        # 3. Fetch full product details (Supabase select is sync)
        products_response = await run_in_threadpool(
            lambda: supabase.table("products").select("*").in_("id", product_ids).execute()
        )
        return products_response.data
        
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        return []
