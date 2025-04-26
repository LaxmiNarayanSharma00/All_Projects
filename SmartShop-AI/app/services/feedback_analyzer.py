from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import RecommendationFeedback
from typing import Dict, Set
import re

class FeedbackAnalyzer:
    def __init__(self, db: Session):
        self.db = db
    
    def extract_rating(self, feedback: str) -> int:
        """Extracts the rating value from the feedback text"""
        match = re.search(r'Rating: (\d+)/5', feedback)
        if match:
            return int(match.group(1))
        return 0
    
    def get_user_feedback_stats(self, user_id: str) -> Dict:
        """Analyzes user feedback statistics"""
        feedbacks = self.db.query(RecommendationFeedback).filter(
            RecommendationFeedback.user_id == user_id
        ).all()
        
        return {
            "average_rating": sum(f.rating for f in feedbacks) / len(feedbacks) if feedbacks else 0,
            "feedback_count": len(feedbacks),
            "low_rated_products": self.get_low_rated_products(user_id)
        }
    
    def get_low_rated_products(self, user_id: str, threshold: int = 3) -> Set[str]:
        """Returns products that the user rated low"""
        low_rated = self.db.query(RecommendationFeedback.product_id).filter(
            RecommendationFeedback.user_id == user_id,
            RecommendationFeedback.rating <= threshold
        ).all()
        return {product_id for (product_id,) in low_rated}
    
    def get_product_feedback_stats(self, product_id: str) -> Dict:
        """Returns feedback statistics for the product"""
        stats = self.db.query(
            func.avg(RecommendationFeedback.rating).label('avg_rating'),
            func.count(RecommendationFeedback.id).label('total_feedbacks')
        ).filter(
            RecommendationFeedback.product_id == product_id
        ).first()
        
        return {
            "average_rating": float(stats.avg_rating) if stats.avg_rating else 0,
            "total_feedbacks": stats.total_feedbacks
        }

    def get_global_feedback_stats(self) -> Dict:
        """Analyzes overall statistics of all feedback"""
        ratings = self.db.query(RecommendationFeedback.rating).all()
        ratings_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for (rating,) in ratings:
            if rating in ratings_distribution:
                ratings_distribution[rating] += 1
        
        return {
            "ratings_distribution": ratings_distribution,
            "total_feedbacks": len(ratings)
        }
