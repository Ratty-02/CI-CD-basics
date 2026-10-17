import joblib

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier


# 1. Load the dataset
iris = load_iris()

X = iris.data
y = iris.target


# 2. Train the model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X, y)


# 3. Save the trained model
joblib.dump(model, "iris_model.joblib")


# 4. Verify the saved model
print("Model trained successfully.")
print("Model saved to iris_model.joblib")

sample = [[5.1, 3.5, 1.4, 0.2]]

prediction = model.predict(sample)

print("Sample prediction:", int(prediction[0]))
print("Class names:", iris.target_names)