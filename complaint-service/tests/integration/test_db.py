import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest, uuid
from database import SessionLocal
import models

def test_create_complaint_db():
    db = SessionLocal()
    c_id = str(uuid.uuid4())
    new_c = models.Complaint(id=c_id, order_id="ord-3", reason="Cold bread")
    db.add(new_c)
    db.commit()
    
    found = db.query(models.Complaint).filter(models.Complaint.id == c_id).first()
    assert found.status == "CREATED"
    db.delete(found)
    db.commit()
    db.close()