import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
import uuid
from database import SessionLocal
import models
def test_create_delivery_db():
    db = SessionLocal()
    delivery_id = str(uuid.uuid4())
    new_del = models.Delivery(
        id=delivery_id, order_id="ord-123", 
        courier_id="c-1", address="Test Addr"
    )
    db.add(new_del)
    db.commit()
    
    found = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    assert found is not None
    assert found.status == "COURIER_ASSIGNED"
    db.delete(found)
    db.commit()
    db.close()

    