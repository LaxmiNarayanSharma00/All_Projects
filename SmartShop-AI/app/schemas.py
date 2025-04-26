from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    id: str
    name: str
    email: str
    age: int
    joined_date: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    id: str
    name: str
    category: str
    brand: str
    price: float
    description: str
    rating: float
    stock: int

    class Config:
        from_attributes = True

class UserBehaviorBase(BaseModel):
    id: str
    user_id: str
    product_id: str
    action: str
    timestamp: datetime

    class Config:
        from_attributes = True

class RecommendationFeedbackCreate(BaseModel):
    user_id: str = Field(..., example="user123")
    product_id: str = Field(..., example="product456")
    rating: int = Field(..., ge=1, le=5, example=4)
    feedback: str = Field(..., example="Great recommendations!")

class RecommendationFeedbackRead(RecommendationFeedbackCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
