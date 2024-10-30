from datetime import datetime, timezone
from extensions import db  # Ensure you have an extensions.py for db setup
from sqlalchemy import Column, Integer, String, DateTime

class Note(db.Model):
    __tablename__ = 'note'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_modified = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
