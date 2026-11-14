import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest, uuid
from database import SessionLocal
import models

def test_create_payment_db():
    db = SessionLocal()
    p_id = str(uuid.uuid4())
    new_p = models.Payment(id=p_id, order_id="ord-1", amount=500)
    db.add(new_p)
    db.commit()
    
    found = db.query(models.Payment).filter(models.Payment.id == p_id).first()
    assert found.amount == 500
    assert found.status == "PENDING"
    db.delete(found)
    db.commit()
    db.close()