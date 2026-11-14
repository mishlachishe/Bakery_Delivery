from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Complaint Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ComplaintCreate(BaseModel):
    orderId: str
    reason: str

@app.post("/api/complaints")
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    new_c = models.Complaint(id=str(uuid.uuid4()), order_id=complaint.orderId, reason=complaint.reason)
    db.add(new_c)
    db.commit()
    db.refresh(new_c)
    return {
        "complaintId": new_c.id,
        "orderId": new_c.order_id,
        "reason": new_c.reason,
        "status": new_c.status,
        "createdAt": new_c.created_at
    }

@app.post("/api/complaints/{id}/review")
def review_complaint(id: str, db: Session = Depends(get_db)):
    c = db.query(models.Complaint).filter(models.Complaint.id == id).first()
    if not c: raise HTTPException(404, "Not found")
    c.status = "REVIEWED"
    db.commit()
    db.refresh(c)
    return {
        "complaintId": c.id,
        "orderId": c.order_id,
        "reason": c.reason,
        "status": c.status,
        "createdAt": c.created_at
    }

@app.post("/api/complaints/{id}/compensate")
def compensate_complaint(id: str, db: Session = Depends(get_db)):
    c = db.query(models.Complaint).filter(models.Complaint.id == id).first()
    if not c: raise HTTPException(404, "Not found")
    c.status = "COMPENSATED"
    db.commit()
    db.refresh(c)
    return {
        "complaintId": c.id,
        "orderId": c.order_id,
        "reason": c.reason,
        "status": c.status,
        "createdAt": c.created_at
    }

@app.post("/api/complaints/{id}/reject")
def reject_complaint(id: str, db: Session = Depends(get_db)):
    c = db.query(models.Complaint).filter(models.Complaint.id == id).first()
    if not c: raise HTTPException(404, "Not found")
    c.status = "REJECTED"
    db.commit()
    db.refresh(c)
    return {
        "complaintId": c.id,
        "orderId": c.order_id,
        "reason": c.reason,
        "status": c.status,
        "createdAt": c.created_at
    }