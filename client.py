import requests


API_URL = "http://127.0.0.1:8000"


# 1. Check service health
health_response = requests.get(
    f"{API_URL}/health",
    timeout=5,
)

print("Health status:", health_response.status_code)
print("Health response:", health_response.json())


# 2. Prepare prediction input
payload = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}


# 3. Send a prediction request
prediction_response = requests.post(
    f"{API_URL}/predict",
    json=payload,
    timeout=10,
)

print("Prediction status:", prediction_response.status_code)
print("Prediction response:", prediction_response.json())