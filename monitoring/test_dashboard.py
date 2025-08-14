from streamlit.testing.v1 import AppTest

def test_app_runs():
    at = AppTest.from_file("./app.py").run()
    assert len(at.exception) == 0