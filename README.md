Iris ML API: Model Serving with FastAPI, Docker and CI

A machine learning model serving project that exposes an Iris flower classifier through a REST API. It combines model training, API development, automated testing, Docker containerization, and continuous integration using GitHub Actions.

Features

Train and serialize a machine learning model.

Serve predictions through a FastAPI REST API.

Validate incoming prediction requests.

Run automated API tests with pytest.

Package the application and model into a Docker image.

Automatically validate code and build the Docker image with GitHub Actions.

Tech Stack

Technology

Purpose

Python

Application and model development

Scikit-learn

Machine learning

FastAPI

REST API development

Uvicorn

ASGI server

Joblib

Model serialization and loading

Pytest

Automated testing

Docker

Application containerization

GitHub Actions

Continuous integration

Project Structure

fastapi-ml-serving/
├── .github/
│   └── workflows/
│       └── ci.yml
├── test/
│   └── test_main.py
├── .dockerignore
├── Dockerfile
├── main.py
├── train.py
├── iris_model.joblib
├── requirements.txt
└── README.md

Prerequisites

Python 3.12

Git

Docker Desktop (for containerized execution)

Getting Started

1. Clone the Repository

git clone https://github.com/Ratty-02/CI-CD-basics.git


2. Create and Activate a Virtual Environment

Windows PowerShell:

py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

3. Install Dependencies

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Model Training

The train.py script trains the model and saves the trained artifact as iris_model.joblib.

python train.py

The API expects the model artifact to exist at the path configured in main.py. If you already have a trained artifact, you can use it without retraining.

Run the API Locally

python -m uvicorn main:app --host 127.0.0.1 --port 8000

API base address:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

API Endpoints

Health Check

GET /health

Checks whether the API is responding.

Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get

Prediction

POST /predict

Accepts four Iris flower measurements and returns a model prediction.

Example request body:

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}

PowerShell example:

$body = @{
    sepal_length = 5.1
    sepal_width = 3.5
    petal_length = 1.4
    petal_width = 0.2
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/predict" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body



Input Validation

The API validates requests according to its configured schema. Requests with missing required fields or values that violate validation rules should be rejected.

Automated Testing

Run the test suite from the project root:

python -m pytest -v

The tests cover API behavior such as the health endpoint, valid predictions, missing fields, and invalid values, depending on the assertions in the test suite.

Docker

Docker packages the application, its dependencies, and the trained model into a container image.

1. Build the Image

Make sure Docker Desktop is running, then execute this from the project root:

docker build -t iris-ml-api .

2. Run the Container

docker run -d --name iris-ml-api-container -p 8000:8000 iris-ml-api

The API should be accessible from the host at http://127.0.0.1:8000.

3. Test the Container

Health check:

Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get

Interactive documentation: http://127.0.0.1:8000/docs

You can test predictions with the PowerShell request shown in the Prediction section.

4. View Logs

docker logs iris-ml-api-container

5. Stop and Remove the Container

docker stop iris-ml-api-container
docker rm iris-ml-api-container

Continuous Integration with GitHub Actions

The workflow is defined in .github/workflows/ci.yml and runs on pushes and pull requests.

The workflow performs these steps:

Checks out the repository.

Sets up Python.

Installs dependencies.

Checks Python syntax.

Runs the pytest suite.

Builds the Docker image.

The Docker build runs only if the earlier steps succeed. If a test fails, the job stops before reaching the Docker build step.

The workflow validates the image build; it does not publish the image to a container registry or deploy the application.

Development Workflow

Train the machine learning model.

Save the model artifact.

Load the artifact in FastAPI.

Test the API locally.

Run automated tests with pytest.

Build and test the Docker container.

Push changes to GitHub.

Let GitHub Actions validate the changes and build the Docker image.

Current Scope

This project demonstrates the fundamentals of model serving and reliable application delivery: model serialization, REST API development, input validation, automated testing, containerization, and continuous integration.


Future Improvements

Deploy the API to a cloud platform.

Publish Docker images to a container registry.

Add API performance and load tests.

Implement structured application logging.

Add model versioning and reproducible training workflows.

Monitor API latency and prediction behavior.

Author

Rehan Azad

GitHub: Ratty-02