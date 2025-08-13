from streamlit.testing.v1 import AppTest

def test_app_runs():
    at = AppTest.from_file("monitoring/app.py").run()
    assert len(at.exception) == 0