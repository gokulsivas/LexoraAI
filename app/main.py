from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import jwt
import bcrypt
from datetime import datetime, timedelta
import os

from app.core.chromadb_manager import chroma_db_manager
from app.core.database import init_db, engine
from app.core.config import settings
from app.routers import api

# Initialize database
init_db()

app = FastAPI(title="LexoraAI", version="1.0.0")

# ✅ Initialize ChromaDB
client, collection = chroma_db_manager.initialize(
    db_path=settings.CHROMA_PATH,
    collection_name="crpc_chapters_chunked"
)

app.state.chroma_db_manager = chroma_db_manager

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= DATABASE SETUP =============

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

# ============= AUTH MODELS =============

JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key_here")

class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str
    confirmPassword: str

class SignInRequest(BaseModel):
    email: str
    password: str

# ============= AUTH ROUTES =============

@app.post("/auth/signup")
async def signup(data: SignUpRequest):
    try:
        if data.password != data.confirmPassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        if len(data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        db = SessionLocal()
        
        # Check if user exists
        existing = db.query(User).filter(
            (User.email == data.email) | (User.username == data.username)
        ).first()
        
        if existing:
            db.close()
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Hash password
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        
        # Create user
        user = User(
            username=data.username,
            email=data.email,
            password_hash=hashed
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate token
        token = jwt.encode(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "exp": datetime.utcnow() + timedelta(days=100)
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        
        db.close()
        
        return {
            "message": "User created successfully",
            "token": token,
            "user": {"id": user.id, "username": user.username, "email": user.email}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/signin")
async def signin(data: SignInRequest):
    try:
        db = SessionLocal()
        
        # Find user
        user = db.query(User).filter(User.email == data.email).first()
        
        if not user:
            db.close()
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not bcrypt.checkpw(data.password.encode(), user.password_hash.encode()):
            db.close()
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate token
        token = jwt.encode(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "exp": datetime.utcnow() + timedelta(days=100)
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        
        db.close()
        
        return {
            "message": "Sign in successful",
            "token": token,
            "user": {"id": user.id, "username": user.username, "email": user.email}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= API ROUTES =============

# Include API router with /api prefix
app.include_router(api.router, prefix="/api", tags=["LexoraAI"])

# ============= HEALTH CHECK =============

@app.get("/")
def health_check():
    try:
        collection = chroma_db_manager.get_collection()
        return {
            "status": "LexoraAI running",
            "chromadb_documents": collection.count(),
            "chromadb_path": settings.CHROMA_PATH,
            "database": "PostgreSQL connected",
            "db_host": settings.DB_HOST
        }
    except Exception as e:
        return {
            "status": "LexoraAI running",
            "error": str(e)
        }
