from flask import Flask, request, jsonify, render_template, session
from pdf2image import convert_from_path
import pytesseract
from query_llm import query_rag
import datetime
import os
from datetime import datetime
from populate_dat import ingest_document_to_db

app = Flask(__name__)
extracted_text = ""  # Store extracted text here


def pdf_to_text(pdf_path):
    pages = convert_from_path(pdf_path, 300)  # DPI setting (adjust as needed)
    all_text = ""
    for page_number, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        all_text += f"Page {page_number + 1}:\n{text}\n\n"
    return all_text


@app.route("/")
def index():
    return render_template("index.html")


app.secret_key = "tarun_acharya"  # Set a secret key for session management

DATA_PATH = "./Read_DIR"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    try:
        # Generate a unique filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(DATA_PATH, filename)

        # Ensure the upload directory exists
        os.makedirs(DATA_PATH, exist_ok=True)

        # Save the file
        file.save(file_path)

        # Store the file path in the session
        session["pdf_path"] = file_path

        ingest_document_to_db(file_path)

        return jsonify({"text": "Upload successful", "file_path": file_path})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/ask", methods=["POST"])
def ask_question():

    question = request.json.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."})
    print("Question asked")
    # Implement a simple response mechanism (can be improved with NLP libraries)
    response = query_rag(question)  # Show first 500 characters as a sample response
    print("Question answered")
    return jsonify({"answer": response})


if __name__ == "__main__":
    app.run(debug=True)
