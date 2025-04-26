import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine, Base, create_tables
from .models import User, Product, UserBehavior, RecommendationFeedback
from .schemas import UserBase, ProductBase, RecommendationFeedbackCreate, RecommendationFeedbackRead
from .services.recommendation_service import RecommendationService
from .utils.data_generator import DataGenerator
from .services.vector_store import VectorStore
import uuid
from datetime import datetime

app = FastAPI()

# Create tables when the application starts
create_tables()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    db_path = "./ecommerce.db"
    chroma_path = "./chroma_db"
    
    # Check if database and vector store exist
    db_exists = os.path.exists(db_path)
    vector_store_exists = os.path.exists(chroma_path)
    
    if not db_exists or not vector_store_exists:
        print("Database or vector store not found. Initializing...")
        
        # Create database tables
        Base.metadata.create_all(bind=engine)
        
        # Generate test data
        db = SessionLocal()
        data_generator = DataGenerator()
        vector_store = VectorStore()
        
        try:
            print("Generating dummy data...")
            
            dummy_data = data_generator.generate_bulk_data(
                num_users=200,
                num_products=2000,
                num_behaviors=10000
            )
            
            # Add Users
            users = [User(**u) for u in dummy_data["users"]]
            db.bulk_save_objects(users)
            
            # Add Products
            products = [Product(**p) for p in dummy_data["products"]]
            db.bulk_save_objects(products)
            
            # Add User Behaviors
            behaviors = [UserBehavior(**b) for b in dummy_data["user_behaviors"]]
            db.bulk_save_objects(behaviors)
            
            # Add Products to Vector Store
            print("Adding products to vector store... (It may take a while)")
            vector_store.add_products(dummy_data["products"])
            
            db.commit()
            print("✅ Dummy data generation completed successfully!")
            print(f"Generated:")
            print(f"- {len(users)} users")
            print(f"- {len(products)} products")
            print(f"- {len(behaviors)} user behaviors")
            
        except Exception as e:
            print(f"❌ Error generating dummy data: {e}")
            db.rollback()
            raise e
        finally:
            db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Shop AI!"}

@app.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: str,
    query: str = None,
    db: Session = Depends(get_db)
) -> Dict:
    try:
        recommendation_service = RecommendationService(db)
        recommendations = await recommendation_service.get_recommendations(
            user_id=user_id,
            query=query
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback", response_model=RecommendationFeedbackRead)
def submit_feedback(feedback: RecommendationFeedbackCreate, db: Session = Depends(get_db)):
    try:
        # Create feedback with generated UUID
        db_feedback = RecommendationFeedback(
            id=str(uuid.uuid4()),
            user_id=feedback.user_id,
            product_id=feedback.product_id,  
            rating=feedback.rating,          
            feedback=feedback.feedback,
            created_at=datetime.utcnow()
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        return db_feedback
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/debug/users", response_model=List[UserBase])
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).limit(5).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/products", response_model=List[ProductBase])
async def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).limit(5).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/generate-data")
async def generate_test_data(db: Session = Depends(get_db)):
    try:
        # First, clear existing data
        db.query(RecommendationFeedback).delete()
        db.query(UserBehavior).delete()
        db.query(Product).delete()
        db.query(User).delete()
        db.commit()

        # Create new data
        from app.utils.data_generator import DataGenerator
        generator = DataGenerator()
        data = generator.generate_bulk_data(
            num_users=100,
            num_products=1000,
            num_behaviors=5000
        )
        
        # Add users
        for user_data in data["users"]:
            user = User(**user_data)
            db.add(user)
        
        # Add products
        for product_data in data["products"]:
            product = Product(**product_data)
            db.add(product)
        
        # Add behaviors
        for behavior_data in data["user_behaviors"]:
            behavior = UserBehavior(**behavior_data)
            db.add(behavior)
        
        db.commit()

        # Return the ID of the first user created
        first_user = db.query(User).first()
        return {
            "message": "Test data generated successfully",
            "test_user_id": first_user.id if first_user else None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/check-user/{user_id}")
async def check_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            # If the user is not found, create new test data
            await generate_test_data(db)
            # Return the first user created
            user = db.query(User).first()
            if not user:
                raise HTTPException(status_code=404, detail="No users found after data generation")
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "message": "New test data generated" if user.id != user_id else "Existing user found"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
