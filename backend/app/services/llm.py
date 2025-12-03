import google.generativeai as genai
from app.core.config import GOOGLE_API_KEY
import logging

# Configure logging
logger = logging.getLogger(__name__)

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set in .env file")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
# User requested gemini-2.5-flash
model = genai.GenerativeModel('gemini-2.5-flash')

async def expand_query(user_query: str) -> str:
    """
    Expands an abstract user query into specific search terms using an LLM.
    """
    prompt = f"""
    You are an expert salesperson for 'Hunnit', a premium activewear brand known for comfort, style, and versatility.
    Your task is to translate the user's abstract query into specific, keyword-rich search terms that would match our product catalog.
    
    Our Catalog Highlights:
    - Collections: Zen (Soft, Flare), Safari Chic (Prints), Cosmic Waves (Bold), Epic Pop (Vibrant).
    - Categories: Leggings, Sports Bras, Crop Tops, Co-ord Sets, Shorts, Skorts, Jackets.
    - Key Features: Moisture Wicking, 4 Way Stretch, Pockets, High Waist, Buttery Soft.
    
    User Query: "{user_query}"
    
    Goal: Identify the best product attributes (category, collection, feature, color) that solve the user's need.
    Return ONLY the expanded search terms as a single string.
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error expanding query: {e}")
        return user_query # Fallback to original query

async def generate_response(user_query: str, context: list) -> str:
    """
    Generates a helpful response explaining why the products match the query.
    """
    if not context:
        return "I couldn't find any products matching your specific requirements. Could you try rephrasing your request?"

    # Format context for the LLM
    context_str = "\n".join([f"- {item['title']} (Price: {item['price']}): {item.get('description', 'No description')}" for item in context])
    
    prompt = f"""
    You are a friendly and knowledgeable salesperson for 'Hunnit', a premium activewear brand.
    The user asked: "{user_query}"
    
    Here are the products from our catalog that match their request:
    {context_str}
    
    Your Goal: Persuade the user that these are the perfect choices for them.
    - Be enthusiastic, warm, and professional.
    - Explicitly link the product features (e.g., "Buttery Soft", "High Waist", "Pockets") to the user's specific needs.
    - If suggesting a Co-ord set, mention how it takes the guesswork out of styling.
    - Keep the tone encouraging and helpful.
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Here are some products that might interest you."
