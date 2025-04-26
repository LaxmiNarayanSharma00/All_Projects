import google.generativeai as genai
from app.config import get_settings
import asyncio
from typing import Dict, List

settings = get_settings()

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    async def generate_recommendation(
        self, 
        user_profile: Dict, 
        products: List,
        feedback_stats: Dict
    ) -> str:
        prompt = f"""
        Based on the user profile, available products, and feedback statistics, 
        generate personalized product recommendations.
        
        User Profile:
        {user_profile}
        
        Feedback Statistics:
        {feedback_stats}
        
        Available Products:
        {products}
        
        Format your response like this:
        
        🎯 TOP RECOMMENDATIONS
        
        1. [Product Name]
           ★ Key Features: [2-3 key features]
           ✨ Why It's Perfect: [1-2 sentences about why this matches the user]
           📊 Feedback Score: [Include if available in feedback stats]
        
        2. [Product Name]
           ★ Key Features: [2-3 key features]
           ✨ Why It's Perfect: [1-2 sentences about why this matches the user]
           📊 Feedback Score: [Include if available in feedback stats]
        
        3. [Product Name]
           ★ Key Features: [2-3 key features]
           ✨ Why It's Perfect: [1-2 sentences about why this matches the user]
           📊 Feedback Score: [Include if available in feedback stats]
        
        💡 PERSONALIZATION INSIGHTS
        • [2-3 bullet points about why these recommendations match the user profile]
        • [Include insights from feedback statistics]
        """
        

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: self.model.generate_content(prompt)
        )
        

        return response.text
