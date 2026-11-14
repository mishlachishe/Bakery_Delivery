from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid, httpx
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Notification Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NotificationCreate(BaseModel):
    clientId: str
    channel: str
    text: str

class ReceiptCreate(BaseModel):
    clientId: str
    orderId: str
    paymentId: str
    amount: int

@app.post("/api/notifications")
def create_notif(notif: NotificationCreate, db: Session = Depends(get_db)):
    new_notif = models.Notification(id=str(uuid.uuid4()), client_id=notif.clientId, channel=notif.channel, text=notif.text)
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return {
        "id": new_notif.id,
        "client_id": new_notif.client_id,
        "channel": new_notif.channel,
        "text": new_notif.text,
        "status": new_notif.status,
        "created_at": new_notif.created_at
    }

@app.post("/api/notifications/receipt")
async def send_receipt(receipt: ReceiptCreate, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"http://localhost:8084/api/payments/{receipt.paymentId}")
            if resp.status_code != 200: raise HTTPException(404, "Payment not found")
            if resp.json()["status"] != "PAID":
                raise HTTPException(400, "Cannot send receipt for unpaid order")
        except httpx.RequestError:
            raise HTTPException(500, "PaymentService is unavailable")

    new_notif = models.Notification(id=str(uuid.uuid4()), client_id=receipt.clientId, channel="email", text=f"Чек на {receipt.amount} руб.")
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return {
        "id": new_notif.id,
        "client_id": new_notif.client_id,
        "channel": new_notif.channel,
        "text": new_notif.text,
        "status": new_notif.status,
        "created_at": new_notif.created_at
    }

@app.get("/api/notifications")
def get_notifications(clientId: str = "", db: Session = Depends(get_db)):
    query = db.query(models.Notification)
    if clientId: query = query.filter(models.Notification.client_id == clientId)
    return query.all()