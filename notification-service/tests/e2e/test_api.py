import requests

BASE_URL = "http://127.0.0.1:8085"
PAYMENT_URL = "http://127.0.0.1:8084"

def test_send_receipt_e2e():
    p_res = requests.post(f"{PAYMENT_URL}/api/payments/invoice", json={"orderId": "o-2", "amount": 100})
    payment_id = p_res.json()["paymentId"]

    bad_payload = {"clientId": "c-2", "orderId": "o-2", "paymentId": payment_id, "amount": 100}
    fail_res = requests.post(f"{BASE_URL}/api/notifications/receipt", json=bad_payload)
    assert fail_res.status_code == 400
    assert fail_res.json()["detail"] == "Cannot send receipt for unpaid order"

    requests.post(f"{PAYMENT_URL}/api/payments/{payment_id}/pay")

    good_res = requests.post(f"{BASE_URL}/api/notifications/receipt", json=bad_payload)
    assert good_res.status_code == 200