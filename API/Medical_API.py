from Services import MedicalService
from Configuration import Config
from flask import Flask, jsonify, request, render_template
from os import walk, path

def create_app(medical_service:MedicalService, config:Config):
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        patients = get_patients()
        return render_template("index.html", patients=patients)

    def get_patients():
        files_path = config.get_ehr_location()
        files_name = next(walk(files_path))[2]
        files_name = list(map(lambda filename: filename.removeprefix("ehr_").removesuffix(".json"), files_name))
        return files_name

    @app.route("/ask", methods=["POST"])
    def ask():
        patient = request.json["patient"]
        question = request.json["question"]
        
        result = medical_service.answer(f"{path.join(config.get_ehr_location(),f"ehr_{patient}.json")}", question)
        return jsonify(result)

    return app