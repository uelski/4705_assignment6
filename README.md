# Sentiment Classification and Monitoring App
This project includes an api directory that houses a sentiment classification model with endpoints to return a sentiment based on the text provided, as well as a monitoring streamlit frontend to view specific statistics from the log file including accuracy and precision. 

## Endpoints
The API has 2 endpoints:

"/health":<br>
- method: GET
- description:<br>
Health check endpoint to verify if the API is running and if the model has been loaded successfully.
- response:<br>
"status": healthy or unhealthy based on if model is None<br>
"message": detail on response

"/predict":<br>
- method: POST
- description:<br>
Predict endpoint to predict the sentiment of the provided review text. Returns a JSON object with the predicted sentiment, "positive" or "negative".
- request body:<br>
"text": The text of the review to get the sentiment of.
"true_label": A string value of a user provided sentiment of what the actual label is, "positive" or "negative".
- response:<br>
"sentiment": string of the sentiment output from the model: "positive" or "negative".

## Monitoring 
The frontend monitoring app includes the following:
- A histogram comparing the distribution of sentence lengths from the IMDB Dataset.csv against the lengths from the logged inference requests.<br>
- A bar chart showing the distribution of predicted sentiments from the logs vs trained sentiments.<br>
- Model accuracy and precision metrics.<br>
- An alert at the top of the app when the accuracy drops below 80%.

## Prerequisites
To get this app up and running Docker and python must be installed on your machine. Postman or 'curl' commands can be used to test the endpoints.

## How To Run
- 'git clone' this repo in project directory of choice.
- 'cd' into this cloned repo.
- Run 'make build' to build the Docker images.
- Run 'make run' to run the Docker containers and create the shared volume.
- The endpoints should now be accessible at http://127.0.0.1:8000 on your machine.
- Use Postman or curl commands to access and test the API endpoints.
- Endpoint documentation can be accessed at http://127.0.0.1:8000/docs.
- Navigate to http://localhost:8501/ to view the frontend streamlit app and associated visualizations.
- Run 'make clean' to remove the Docker image.

## How To Test
With Curl:<br>
- `curl http://127.0.0.1:8000/health`
- `curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d '{"text": "This movie was excellent!", "true_label": "positive"}'`

With Postman:<br>
- GET request
- url: "http://127.0.0.1:8000/health"
- POST request
- url: "http://127.0.0.1:8000/predict"
- body:
    - type: raw (JSON)
    - {"text": "This movie was excellent!", "true_label": "positive"}

Evaluation Script:
- From the root directory run 'python evaluation.py' to populate the logs file and view the frontend with new data. This script will run through a provided json file, make requests to the api /predict endpoint which in turn will populate the log files. After running this script, navigate to the frontend at http://localhost:8501/ and refresh the page to view the most recent log statistics.