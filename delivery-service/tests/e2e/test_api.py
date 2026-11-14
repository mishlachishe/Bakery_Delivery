import requests
import uuid

BASE_URL = "http://127.0.0.1:8083"

def test_create_delivery_api():
    order_resp = requests.post("http://127.0.0.1:8081/api/orders", json={
        "clientId": "test-e2e", "items": "test", "deliveryAddress": "E2E Address", "total": 100
    })
    order_id = order_resp.json()["orderId"]

    payload = {"orderId": order_id, "courierId": "courier-e2e"}
    response = requests.post(f"{BASE_URL}/api/deliveries", json=payload)
    
    assert response.status_code == 200
    body = response.json()
    assert body["address"] == "E2E Address"
    assert body["status"] == "COURIER_ASSIGNED"