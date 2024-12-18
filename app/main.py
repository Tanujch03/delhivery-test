from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .models import User
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel,EmailStr
from app.database import get_db


Base.metadata.create_all(bind=engine)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    
    
app = FastAPI()
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Replace "*" with specific methods as needed
    allow_headers=["*"],  # Replace "*" with specific headers as needed
)



@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with the same email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new user instance
    new_user = User(name=user.name, email=user.email)
    
    # Add to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user