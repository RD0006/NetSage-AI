from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from checker.checker import run_checks
from llm.provider import generate_diagnosis
from models.schemas import AnalyzeRequest, Diagnosis


app = Flask(__name__)

CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "NetSage AI backend is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required."
            }), 400

        # Validate incoming request
        validated_request = AnalyzeRequest(**data)

        request_data = validated_request.model_dump()

        # ---------------------------------------------
        # Step 1: Deterministic rule checking
        # ---------------------------------------------

        checker_result = run_checks(request_data)

        # ---------------------------------------------
        # Step 2: LLM diagnosis
        # ---------------------------------------------

        raw_diagnosis = generate_diagnosis(
            request_data,
            checker_result
        )

        # ---------------------------------------------
        # Step 3: Parse LLM JSON
        # ---------------------------------------------

        try:
            diagnosis_data = json.loads(raw_diagnosis)
        except json.JSONDecodeError:
            return jsonify({
                "error": "LLM returned invalid JSON.",
                "raw_response": raw_diagnosis,
                "checker": checker_result
            }), 502

        # ---------------------------------------------
        # Step 4: Validate diagnosis schema
        # ---------------------------------------------

        try:
            diagnosis = Diagnosis(**diagnosis_data)
        except Exception as e:
            return jsonify({
                "error": "LLM diagnosis does not match the required schema.",
                "details": str(e),
                "raw_response": diagnosis_data,
                "checker": checker_result
            }), 502

        # ---------------------------------------------
        # Step 5: Return final response
        # ---------------------------------------------

        return jsonify({
            "checker": checker_result,
            "diagnosis": diagnosis.model_dump()
        }), 200

    except Exception as e:

        return jsonify({
            "error": "Internal server error.",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )