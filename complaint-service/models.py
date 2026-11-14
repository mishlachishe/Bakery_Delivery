from sqlalchemy import Column, String, DateTime
from datetime import datetime
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(String, primary_key=True)
    order_id = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="CREATED")
    created_at = Column(DateTime, default=datetime.utcnow)