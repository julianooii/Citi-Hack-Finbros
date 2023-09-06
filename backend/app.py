import json
from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import os 
from dotenv import load_dotenv
import pytesseract
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import openai


load_dotenv()

app = Flask(__name__)
CORS(app)


def get_db():
    client = MongoClient(host = 'mongodb',
                         port = 27017)
    
    db = client["citi_finbros_db"]
    return db

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0,
    
    max_tokens=150,

    )

    return response.choices[0].message["content"]

@app.route('/')
def home():
    return "Hello World!"

#create a user
@app.route("/user", methods=["POST"])
def create_user():
    db = get_db()
    data = json.loads(request.data)
    db.users.insert_one(data)
    return jsonify({"message": "User Created"})

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the 'file' field exists in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if the user submitted an empty file
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Check if the file is a PDF
        if file and file.filename.endswith('.pdf'):
            # Save the PDF to a temporary location
            pdf_path = './temp.pdf'
            file.save(pdf_path)

            # Convert the PDF to an image (you may need to install pdf2image)
            print("converting pdf to image")
            images = convert_from_path(pdf_path)

            print("converting pdf to image SUCCESS")

            # Initialize text to store the OCR result
            text = ''

            for img in images:
                # Perform OCR on each image
                text += pytesseract.image_to_string(img)
            # Optionally, you can save the OCR result to a file or process it further

            return jsonify({'result': text})
        else:
            return jsonify({'error': 'Invalid file format. Only PDF files are supported.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/coref", methods=["POST"])
def coref():
    openai.api_key = os.getenv("OPENAI_APIKEY")
    db = get_db()
    data = json.loads(request.data)
    query = data['query']
    training = "Use coreference resolution in NLP to resolve this text, making sure every pronoun explicitly states the subject: "
    prompt = training + query
    response = get_completion(prompt)
    return jsonify({"message": response})

@app.route("/rdf", methods=["POST"])
def rdf():
    openai.api_key = os.getenv("OPENAI_APIKEY")
    db = get_db()
    data = json.loads(request.data)
    query = data['query']
    training = "Organise this text to produce a RDF triple and output it in a python dictionary format without any text formatting: "
    prompt = training + query
    response = get_completion(prompt)
    return jsonify({"message": response})

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
