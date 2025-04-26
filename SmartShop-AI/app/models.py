from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from datetime import datetime
from .database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    rating = Column(Float)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    joined_date = Column(DateTime, default=datetime.utcnow)

class UserBehavior(Base):
    __tablename__ = "user_behaviors"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)
    category = Column(String, nullable=False)  # Kategori alanını ekledik
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserBehavior(id={self.id}, user_id={self.user_id}, action={self.action})>"

class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedbacks"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)  # Yeni eklendi
    rating = Column(Integer, nullable=False)  # Yeni eklendi
    feedback = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RecommendationFeedback(id={self.id}, user_id={self.user_id}, rating={self.rating})>"
