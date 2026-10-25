
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# Find the saved model relative to this file
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "model_bundle.joblib"

# Load the model once when the API starts
bundle = joblib.load(MODEL_PATH)

model = bundle["model"]
feature_columns = bundle["feature_columns"]
class_names = bundle["class_names"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": bundle["selected_model"]
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a JSON object containing the input features."
        }), 400

    missing = [col for col in feature_columns if col not in data]

    if missing:
        return jsonify({
            "error": "Missing required features.",
            "missing_features": missing
        }), 400

    try:
        # Keep exactly the feature names and order used during training
        input_df = pd.DataFrame(
            [[data[col] for col in feature_columns]],
            columns=feature_columns
        )

        prediction = int(model.predict(input_df)[0])

        result = {
            "prediction": prediction,
            "class": class_names[prediction],
            "model": bundle["selected_model"]
        }

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            result["probabilities"] = {
                class_names[int(label)]: round(float(probability), 4)
                for label, probability in zip(
                    model.classes_, probabilities
                )
            }

        return jsonify(result)

    except (TypeError, ValueError) as exc:
        return jsonify({
            "error": "Invalid feature values.",
            "details": str(exc)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
