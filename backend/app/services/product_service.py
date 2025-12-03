from app.core.db import supabase
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ProductService:
    @staticmethod
    def get_products(limit: int, offset: int) -> List[Dict[str, Any]]:
        """
        Fetch a list of products with pagination.
        """
        try:
            response = supabase.table("products").select("*").range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise e

    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a single product by ID.
        """
        try:
            response = supabase.table("products").select("*").eq("id", product_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {e}")
            raise e

    @staticmethod
    def get_products_by_ids(product_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch multiple products by their IDs.
        """
        try:
            if not product_ids:
                return []
            response = supabase.table("products").select("*").in_("id", product_ids).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching products by IDs: {e}")
            raise e
