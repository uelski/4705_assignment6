import json
import requests
from sklearn.metrics import accuracy_score
import pandas as pd

'''
Create this script in the root directory of your project.

Use the test_data.json file: [{"text": "...", "true_label": "positive"}, ...]. (Provided at the end of this page)

Your script must read the file, loop through each item, send the text to the running FastAPI service's /predict endpoint (e.g., at http://localhost:8000/predict), and print a final accuracy score.

You may use the requests library from Python to do this.
'''

# read file
with open("test.json", "r") as f:
    test_data = json.load(f)

# setup for accuracy evaluation
y_true = []
y_pred = []

for item in test_data:
    payload = {
        "text": item["text"],
        "true_label": item["true_label"]
    }

    try:
        # send POST with both text and true_label in body
        response = requests.post("http://localhost:8000/predict", json=payload)

        result = response.json()
        prediction = result.get("sentiment")

        if prediction:
            y_true.append(item["true_label"])
            y_pred.append(prediction)
        else:
            # print error
            print('error on prediction')
            pass
    except Exception as e:
        # print error
        print('exception on post', e)
        pass

# compute and print accuracy
accuracy = accuracy_score(y_true, y_pred)
print(f"Model Accuracy: {accuracy:.2%}")