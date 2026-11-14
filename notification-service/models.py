from sqlalchemy import Column, String, DateTime
from datetime import datetime
from database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True)
    client_id = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    text = Column(String, nullable=False)
    status = Column(String, default="SENT") # По умолчанию отправлено
    created_at = Column(DateTime, default=datetime.utcnow)