from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import Document, QueryLog
from app.models.schemas import DocumentCreate, QueryLogCreate

router = APIRouter()

@router.post("/documents")
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.post("/query-logs")
def log_query(query: QueryLogCreate, db: Session = Depends(get_db)):
    db_query = QueryLog(**query.dict())
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

@router.get("/query-logs")
def get_query_logs(db: Session = Depends(get_db)):
    return db.query(QueryLog).all()
