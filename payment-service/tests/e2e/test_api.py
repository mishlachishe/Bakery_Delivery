import requests
BASE_URL = "http://127.0.0.1:8084"

def test_payment_flow():
    res = requests.post(f"{BASE_URL}/api/payments/invoice", json={"orderId": "o-1", "amount": 300})
    assert res.status_code == 200
    payment_id = res.json()["paymentId"]
    
    pay_res = requests.post(f"{BASE_URL}/api/payments/{payment_id}/pay")
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "PAID"
    print(pay_res)