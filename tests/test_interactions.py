# test_interactions.py

import json
from fastapi.testclient import TestClient
from Adventurator.app import app

client = TestClient(app)

def test_missing_headers_401():
    r = client.post("/interactions", data=b"{}")
    assert r.status_code == 401
