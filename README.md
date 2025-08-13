# Sentiment Classification and Monitoring App
This project includes an api directory that houses a sentiment classification model with endpoints to return a sentiment based on the text provided, as well as a monitoring streamlit frontend to view specific statistics from the log file including accuracy and precision. 

## Architecture
This repo includes both a frontend (/monitoring) and backend (/api) application, unit tests for both, Dockerfiles, a Makefile and Github Actions as part of a CI/CD pipeline, and deployed via AWS EC2. The backend application was built using FastAPI and includes two endpoints as defined below. Crucially, the POST "/predict" endpoint includes code to write to a log file that is shared via a docker volume with the frontend application. The frontend application was built using Streamlit and includes code to connect to the shared volume with the logs file, and display specific statistics related to the training data and logs. It also includes an alert banner if the computed accuracy falls below a certain threshold of 80%. The applications can easily be run by cloning and following the 'Local Development' section below using the Makefile which in turn leverages the individual Dockerfiles for each sub-directory, /monitoring and /api. A Github Action workflow has been setup to run the unit tests for each directory via pytest, and uses 'ruff' to lint the python code. This ensures code quality and passing tests before new development work is merged into the 'main' branch. Finally, steps below outline how to setup and run this repository on an AWS EC2 instance and connect via your local machine to both the frontend Streamlit app, and the backend FastAPI endpoints via curl and Postman.

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

## Local Development
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

## Manual Deployment Guide
These are the directions to create an AWS EC2 instance, connect via ssh, and build and run the applications from this repository. 

Create an EC2 Instance:
- In the AWS Management Console search and navigate to the EC2 console.
- Select launch instance
- Give your instance a name - ie Monitoring App
- Select the Amazon Linux 2023 AMI under the Application and OS Images section
- Under instance type select t2.micro
- Under Key pair (login) select a key pair that you already have a downloaded .pem file for, or create a new key pair and download and save the .pem file to a specific location to use later.
- This step is important because you will need your .pem file to ssh into the ec2 instance
- Under Network Settings click the Edit button on the top right to set security group details. We need to set three rules, one for SSH via your IP, one to access port 8000 for the FastAPI and one to access port 8501 for the Streamlit app.
- Set type: SSH, Protocol/Port: TCP 22, Source: My IP (auto-fills your public IPv4)
- Set type: Custom TCP, Port range: 8000, Source (IPv4): 0.0.0.0/0
- Set type: Custom TCP, Port range: 8501, Source (IPv4): 0.0.0.0/0
- Finally, select 'Launch Instance'

Now you can connect to your instance, download the necessary packages, git clone, and run the applications in your EC2 instance.
- navigate to the instance details by going to EC2 dashboard and clicking on the newly created instance
- view the public ipv4 address by clicking on the instance and viewing it's details. You will need this address later.
- go to a new terminal window on your machine and navigate to the directory you saved your .pem file
- run 'chmod 400 your-key.pem' to secure your key pair.
- run 'ssh -i your-key.pem ec2-user@\<EC2-Public-IP>' - replacing \<EC2-Public-IP> with your instance's public IP.
- this information to connect to your specific address is available in the AWS EC2 console at the EC2 instance under the 'Connect' option and 'SSH client'
- You should now be connected to your EC2 instance via the terminal window.
- Install Docker (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-docker.html):
    - 'sudo yum update -y'
    - 'sudo yum install -y docker'
    - 'sudo service docker start'
    - 'sudo usermod -a -G docker ec2-user'
    - "Pick up the new docker group permissions by logging out and logging back in again. To do this, close your current SSH terminal window and reconnect to your instance in a new one. Your new SSH session should have the appropriate docker group permissions."
    - check permissions and docker working:
        - 'docker ps'
- install git:
    - 'sudo yum install git -y'
    - 'git --version'
- install make to run the Makefile:
    - 'sudo yum groupinstall "Development Tools"'

Now you should have all of the necessary tools installed on your EC2 instance to run the applications.
- follow the 'Local Development' section of this readme:
    - git clone the repo on the ec2 instance
    - cd into the repo
    - 'make build'
    - 'make run'
- to access the applications from your machine:
    - navigate to http://\<EC2-PUBLIC-IP>:8501 for the streamlit monitoring app
    - navigate to http://\<EC2-PUBLIC-IP>:8000/docs to view the docs for the FastAPI app
    - in Postman interact with the endpoints located at:
        - GET http://\<EC2-PUBLIC-IP>:8000/health
        - POST http://\<EC2-PUBLIC-IP>:8000/predict
- to remove the Docker images from the EC2 instance run 'make clean'
- to exit the ssh connection run 'exit' in the terminal shell you are currently using to connect

That is it! You should now be able to connect to your EC2 instance via ssh and run the applications within this repository. 