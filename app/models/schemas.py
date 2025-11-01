from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DocumentBase(BaseModel):
    filename: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    chromadb_id: Optional[str]
    indexed: bool
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class QueryLogCreate(BaseModel):
    question: str
    answer: str
    sources: List[dict]

class QueryLog(QueryLogCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
