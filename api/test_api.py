import pytest
import main
import tempfile
from fastapi.testclient import TestClient

# to handle log file in main.py
real_open = open
tmp_log = tempfile.NamedTemporaryFile(delete=False)

def _fake_open(path, mode="r", *args, **kwargs):
    if isinstance(path, str) and path.endswith("prediction_logs.json"):
        return real_open(tmp_log.name, mode, *args, **kwargs)
    return real_open(path, mode, *args, **kwargs)

main.open = _fake_open

client = TestClient(main.app)

def test_predict_positive():
    r = client.post("/predict", json={"text": "This is a great movie!", "true_label": "positive"})
    assert r.status_code == 200
    assert "sentiment" in r.json() 

def test_predict_negative():
    r = client.post("/predict", json={"text": "This is a terrible movie.", "true_label": "negative"})
    assert r.status_code == 200
    assert "sentiment" in r.json()

def test_predict_malformed():
    r = client.post("/predict", json={"text": "This should fail."})
    assert r.status_code == 422