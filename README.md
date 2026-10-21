Iris ML Model Serving API

A machine-learning model serving project that exposes a trained Iris classifier through a FastAPI REST API. The project includes automated tests, Docker packaging, Kubernetes deployment manifests, and Prometheus instrumentation for monitoring API requests.

Features

Serve predictions from a trained scikit-learn Iris classifier.

Validate prediction inputs with Pydantic.

Health-check endpoint at /health.

Prediction endpoint at /predict.

Prometheus metrics endpoint at /metrics.

Automated API tests with pytest.

Docker image for consistent application packaging.

Kubernetes Deployment and Service manifests.

Prometheus configuration for scraping API metrics.

Technology Stack

Python 3.12

FastAPI and Uvicorn

scikit-learn and joblib

pytest and HTTPX

Docker

Kubernetes (kubectl)

Prometheus

Grafana (for dashboard visualization)

Project Structure

fastapi-ml-serving/
├── .github/
│   └── workflows/
│       └── ci.yml
├── K8/
│   ├── deployment.yaml
│   └── service.yaml
├── monitoring/
│   └── prometheus.yml
├── test/
│   └── test_main.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── client.py
├── env_test.py
├── iris_model.joblib
├── main.py
├── README.md
├── requirements.txt
└── train.py



Prerequisites

Install the following before running the project:

Python 3.12

Git

Docker Desktop (for Docker and its local Kubernetes cluster)

kubectl (for Kubernetes deployment)

Prometheus and Grafana if you want to run monitoring separately

1. Clone the Repository

Replace <your-github-username> with your GitHub username:

git clone https://github.com/<your-github-username>/fastapi-ml-serving.git
cd fastapi-ml-serving

If you already have the repository locally, skip this step.

2. Set Up Python

On Windows PowerShell:

py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

If PowerShell blocks activation, you can run this in the current terminal session and retry activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1

3. Run the API Locally

From the project root:

uvicorn main:app --reload

The API will normally be available at http://localhost:8000.

Interactive API documentation is available at http://localhost:8000/docs.

Health Check

Invoke-RestMethod http://localhost:8000/health

Expected response:

{
  "status": "healthy"
}

Make a Prediction

In PowerShell:

$body = @{
    sepal_length = 5.1
    sepal_width  = 3.5
    petal_length = 1.4
    petal_width  = 0.2
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:8000/predict" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

The response contains a numeric class prediction. The class mapping depends on how the model was trained.

Metrics

With the API running, open http://localhost:8000/metrics or query it from PowerShell:

(Invoke-WebRequest http://localhost:8000/metrics).StatusCode

The endpoint exposes Prometheus metrics produced by the FastAPI instrumentator.

4. Run Automated Tests

From the project root with the virtual environment activated:

python -m pytest -v

The current test suite covers the health endpoint, a valid prediction request, a missing input field, and an invalid feature value.

5. Build and Run with Docker

Build the image:

docker build -t iris-ml-api:v1 .

Run the container:

docker run --rm --name iris-ml-api-container -p 8000:8000 iris-ml-api:v1

Keep the terminal running. In another PowerShell window, test the API:

Invoke-RestMethod http://localhost:8000/health

If port 8000 is already in use, stop the process or container using it, or map a different local port, such as -p 8001:8000. Then use http://localhost:8001.

6. Kubernetes Deployment

The Kubernetes manifests are in K8/.

Make sure Docker Desktop Kubernetes is enabled and running, and that the image iris-ml-api:v1 is available to the local cluster. From the project root:

kubectl apply -f .\K8\deployment.yaml
kubectl apply -f .\K8\service.yaml
kubectl rollout status deployment/iris-ml-api --timeout=120s
kubectl get deployments
kubectl get pods -o wide
kubectl get services

The Service is configured as a NodePort Service. The manifest uses NodePort 30080; actual access depends on the local Kubernetes setup.

For a reliable local test, forward the Service port:

kubectl port-forward service/iris-ml-api 8001:8000

Keep that terminal open and test from another terminal:

Invoke-RestMethod http://localhost:8001/health

Stop port forwarding with Ctrl+C.

7. Prometheus and Grafana

The Prometheus scrape configuration is located at monitoring/prometheus.yml.

Review the target address in that file and make sure it is reachable from the Prometheus container, not just from your Windows host. For example, localhost inside a Prometheus container refers to that container itself. The correct target depends on how the API is running (Docker, host process, or Kubernetes).

Open the Prometheus UI at http://localhost:9090 if Prometheus is running there. Go to Status → Targets and confirm the API target is UP.

Example PromQL queries (metric names and labels depend on the installed instrumentation version and configuration):

http_requests_total

Request rate over one minute:

rate(http_requests_total[1m])

Average request duration, if the corresponding duration metrics are exposed:

rate(http_request_duration_seconds_sum[5m])
/
rate(http_request_duration_seconds_count[5m])

Open Grafana at http://localhost:3000 if it is running. Configure Prometheus as a data source and create panels using the metrics available in your Prometheus instance. Use the credentials configured for your local Grafana instance.

8. GitHub Actions

The repository contains a workflow at .github/workflows/ci.yml. Check the Actions tab of your GitHub repository to see the latest run and confirm the workflow performs the expected checks and tests.

Model and Training

train.py contains the model-training script.

iris_model.joblib is the serialized model loaded by main.py.

The model artifact must be present at the path expected by the application. Retraining the model does not automatically update a running Docker image or Kubernetes Deployment; rebuild and redeploy the application when you want to serve a new artifact.

Current Scope and Limitations

This is a learning and demonstration project, not a hardened production service.

The API returns the model's numeric class prediction; a human-readable label mapping can be added if needed.

The Kubernetes manifests are intended for a local development cluster and are not a complete production deployment configuration.

Monitoring availability depends on the Prometheus target being correctly configured for the environment in which the API runs.

Production deployment would require additional work such as versioned model artifacts, configuration and secret management, resource limits, security controls, and deployment validation.

Troubleshooting

Model file not found

Run commands from the project root and confirm iris_model.joblib exists. The application currently loads the model using a relative path.

Port already in use

Use a different local port mapping, such as Docker -p 8001:8000, and call the API on that local port.

Kubernetes image pull error

Check that the Deployment's image name matches a locally available image and that the image is available to the Kubernetes cluster. For a remote cluster, push the image to a registry the cluster can access.

Prometheus target is down

Check the target address in monitoring/prometheus.yml, confirm the API exposes /metrics, and verify the target is reachable from the Prometheus container or environment.
