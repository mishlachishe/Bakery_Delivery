from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import httpx, uuid
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Delivery Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DeliveryCreate(BaseModel):
    orderId: str
    courierId: str

@app.post("/api/deliveries")
async def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://localhost:8081/api/orders/{delivery.orderId}")
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Order not found")
            address = response.json()["deliveryAddress"]
        except Exception:
            raise HTTPException(status_code=500, detail="Error connecting to OrderService")

    new_delivery = models.Delivery(
        id=str(uuid.uuid4()), order_id=delivery.orderId,
        courier_id=delivery.courierId, address=address
    )
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    
    return {
        "deliveryId": new_delivery.id,
        "orderId": new_delivery.order_id,
        "courierId": new_delivery.courier_id,
        "address": new_delivery.address,
        "status": new_delivery.status
    }

@app.post("/api/routes")
def build_route():
    return {"routeId": str(uuid.uuid4()), "points": ["ул. Пушкина, 10", "ул. Ленина, 5"]}

@app.put("/api/routes/{id}/optimize")
def optimize_route(id: str):
    return {"routeId": id, "totalDistance": 5400}

@app.post("/api/deliveries/{id}/complete")
def complete_delivery(id: str, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    delivery.status = "DELIVERED"
    db.commit()
    db.refresh(delivery)
    return {
        "deliveryId": delivery.id,
        "orderId": delivery.order_id,
        "courierId": delivery.courier_id,
        "address": delivery.address,
        "status": delivery.status
    }