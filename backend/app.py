from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pdf_reader import extract_text
from ai_agent import extract_essential_data

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_pdfs():
    files = request.files.getlist("files")
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Step 1: Extract text from PDF
        text = extract_text(file_path)

        # Step 2: Send text to AI Agent
        json_data = extract_essential_data(text)

        results.append({
            "file_name": file.filename,
            "extracted_data": json_data
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)