from .vector_store import VectorStore
from .gemini_service import GeminiService
from .feedback_analyzer import FeedbackAnalyzer
from sqlalchemy.orm import Session
from app.models import User, UserBehavior
from typing import Dict
import asyncio
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = VectorStore()
        self.feedback_analyzer = FeedbackAnalyzer(db)
        self.gemini_service = GeminiService()
        self.cache = {}
        self.cache_timeout = timedelta(minutes=5)
    
    def _get_cache_key(self, user_id: str, query: str = None) -> str:
        return f"{user_id}:{query or 'default'}"
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        return datetime.utcnow() - timestamp < self.cache_timeout
    
    async def _get_user_profile_async(self, user_id: str) -> Dict:
        """Get user profile asynchronously"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        behaviors = self.db.query(UserBehavior).filter(
            UserBehavior.user_id == user_id
        ).all()
        

        category_counts = {}
        total_purchases = 0
        for behavior in behaviors:
            if behavior.category in category_counts:
                category_counts[behavior.category] += 1
            else:
                category_counts[behavior.category] = 1
            total_purchases += 1
        
        return {
            "user_info": {
                "id": user.id,
                "age": user.age
            },
            "behavior_summary": {
                "total_purchases": total_purchases,
                "favorite_categories": category_counts
            }
        }

    async def _get_feedback_stats_async(self, user_id: str) -> Dict:
        """Get feedback statistics asynchronously"""
        return self.feedback_analyzer.get_user_feedback_stats(user_id)

    async def get_recommendations(self, user_id: str, query: str = None) -> Dict:
        """Create personalized recommendations for a user"""
        cache_key = f"{user_id}:{query or 'default'}"
        
        # Cache control
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if datetime.utcnow() - timestamp < self.cache_timeout:
                return data

        try:
            # Create tasks for parallel operations
            user_profile_task = asyncio.create_task(self._get_user_profile_async(user_id))
            feedback_stats_task = asyncio.create_task(self._get_feedback_stats_async(user_id))
            
            # Wait for parallel operations
            user_profile = await user_profile_task
            feedback_stats = await feedback_stats_task
            
            # Get low-rated products
            low_rated_products = feedback_stats["low_rated_products"]
            
            # Search similar products with vector search
            if query:
                similar_products = self.vector_store.search_similar_products(query, n_results=10)
            else:
                favorite_categories = user_profile["behavior_summary"]["favorite_categories"]
                default_category = next(iter(favorite_categories)) if favorite_categories else "Electronics"
                similar_products = self.vector_store.search_similar_products(f"best products in {default_category}", n_results=10)
            
            # Filter low-rated products
            filtered_products = {
                "ids": [],
                "documents": [],
                "metadatas": [],
                "distances": []
            }
            
            for i, product_id in enumerate(similar_products["ids"]):
                if product_id not in low_rated_products:
                    filtered_products["ids"].append(product_id)
                    filtered_products["documents"].append(similar_products["documents"][i])
                    filtered_products["metadatas"].append(similar_products["metadatas"][i])
                    if similar_products.get("distances"):
                        filtered_products["distances"].append(similar_products["distances"][i])
            
            # Get first 5 products
            for key in filtered_products:
                filtered_products[key] = filtered_products[key][:5]
            
            # Add feedback statistics for each product
            for metadata in filtered_products["metadatas"]:
                product_id = filtered_products["ids"][filtered_products["metadatas"].index(metadata)]
                product_feedback_stats = self.feedback_analyzer.get_product_feedback_stats(product_id)
                metadata["feedback_stats"] = product_feedback_stats
            
            # Get global feedback statistics
            global_feedback_stats = self.feedback_analyzer.get_global_feedback_stats()
            
            result = {
                "user_profile": user_profile,
                "recommendations": await self.gemini_service.generate_recommendation(
                    user_profile=user_profile,
                    products=filtered_products,
                    feedback_stats=feedback_stats
                ),
                "similar_products": filtered_products,
                "feedback_stats": global_feedback_stats
            }
            
            # Cache the result
            self.cache[cache_key] = (result, datetime.utcnow())
            
            return result
            
        except Exception as e:
            logger.error(f"Error in get_recommendations: {str(e)}")
            raise
