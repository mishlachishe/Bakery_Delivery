import requests
BASE_URL = "http://127.0.0.1:8086"

def test_complaint_flow():
    res = requests.post(f"{BASE_URL}/api/complaints", json={"orderId": "o-3", "reason": "Bad quality"})
    assert res.status_code == 200
    c_id = res.json()["complaintId"]

    reject_res = requests.post(f"{BASE_URL}/api/complaints/{c_id}/reject", json={"reason": "Client is wrong"})
    assert reject_res.status_code == 200
    assert reject_res.json()["status"] == "REJECTED"

