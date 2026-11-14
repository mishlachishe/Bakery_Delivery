
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest, uuid
from database import SessionLocal
import models

def test_create_notification_db():
    db = SessionLocal()
    n_id = str(uuid.uuid4())
    new_n = models.Notification(id=n_id, client_id="c-1", channel="sms", text="Hello")
    db.add(new_n)
    db.commit()
    
    found = db.query(models.Notification).filter(models.Notification.id == n_id).first()
    assert found.status == "SENT"
    db.delete(found)
    db.commit()
    db.close()