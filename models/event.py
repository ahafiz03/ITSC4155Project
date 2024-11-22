from extensions import db  # Import the db object from your extensions.py
from sqlalchemy import Column, Integer, String

class Event(db.Model):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    start = Column(String(10), nullable=False)

    def __repr__(self):
        return f"<Event {self.title}>"
