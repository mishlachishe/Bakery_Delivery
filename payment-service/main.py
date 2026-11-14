from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Payment Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PaymentCreate(BaseModel):
    orderId: str
    amount: int

@app.post("/api/payments/invoice")
def create_invoice(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = models.Payment(
        id=str(uuid.uuid4()), 
        order_id=payment.orderId, 
        amount=payment.amount,
        status="PENDING"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return {
        "paymentId": new_payment.id,
        "orderId": new_payment.order_id,
        "amount": new_payment.amount,
        "status": new_payment.status
    }

@app.post("/api/payments/{id}/pay")
def pay(id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == id).first()
    if not payment: raise HTTPException(404, "Not found")
    payment.status = "PAID"
    db.commit()
    db.refresh(payment)
    return {
        "paymentId": payment.id,
        "orderId": payment.order_id,
        "amount": payment.amount,
        "status": payment.status
    }

@app.post("/api/payments/{id}/refund")
def refund(id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == id).first()
    if not payment: raise HTTPException(404, "Not found")
    payment.status = "REFUNDED"
    db.commit()
    db.refresh(payment)
    return {
        "paymentId": payment.id,
        "orderId": payment.order_id,
        "amount": payment.amount,
        "status": payment.status
    }

@app.get("/api/payments/{id}")
def get_payment(id: str, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == id).first()
    if not payment: raise HTTPException(404, "Not found")
    return {
        "paymentId": payment.id,
        "orderId": payment.order_id,
        "amount": payment.amount,
        "status": payment.status
    }