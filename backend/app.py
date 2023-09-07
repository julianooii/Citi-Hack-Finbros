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
import spacy
import msal
import webbrowser
from msal import PublicClientApplication
import requests


load_dotenv()

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")


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
def coref(query):
    openai.api_key = os.getenv("OPENAI_APIKEY")
    db = get_db()
    training = "Use coreference resolution in NLP to resolve this text, making sure every pronoun explicitly states the subject: "
    prompt = training + query
    response = get_completion(prompt)
    return response

@app.route("/rdf", methods=["POST"])
def rdf(query):
    # openai.api_key = os.getenv("OPENAI_APIKEY")
    db = get_db()
    # training = "Organise this text to produce a RDF triple and output it in a python dictionary format without any text formatting: "
    # prompt = training + query
    # response = get_completion(prompt)
    doc = nlp(query)
    triples = []
    for sent in doc.sents:
        subject = None
        verb = None
        obj = None

        for token in sent:
            if "subj" in token.dep_:
                # Check for compound nouns to capture multi-word subjects
                subject = " ".join([t.text for t in token.subtree])
            elif token.pos_ == "VERB":
                verb = token.text
            elif "obj" in token.dep_:
                # Check for compound nouns to capture multi-word objects
                obj = " ".join([t.text for t in token.subtree])

        # If subject, verb, and object are found, add the triple
        if subject and verb and obj:
            triples.append((subject, verb, obj))

    # Print the extracted triples
    # for triple in triples:
    #     print(triple)

    return triples

@app.route("/query", methods=["POST"])
def query():
    db = get_db()
    data = json.loads(request.data)
    query = data['query']
    coref_text = coref(query)
    rdf_text = rdf(coref_text)
    return jsonify({"message": rdf_text})


@app.route("/oneDriveAuth", methods=['POST']) # {"message" : "Documents"}
def MicrosoftAuth():
    APPLICATION_ID = "27f17a4b-5e7e-477e-866f-6eff3e3aa049"
    base_url = "https://graph.microsoft.com/v1.0/"

    scopes = ['Files.Read', 'Files.Read.All']

    data = json.loads(request.data)
    folder_dir = data['message']

    app = msal.PublicClientApplication(
        APPLICATION_ID,
    )
    flow = app.initiate_device_flow(scopes=scopes)
    print(flow['message'])
    print(flow['message'].split()[-3])

    return jsonify({"message": [flow['message'].split()[-3], flow, folder_dir]}) #format is {"message": [code, flow, folder]}



@app.route("/oneDriveFileExtract", methods=['POST']) #format is {"message": [code, flow, folder]}
def MicrosoftAuth2():
    APPLICATION_ID = "27f17a4b-5e7e-477e-866f-6eff3e3aa049"
    base_url = "https://graph.microsoft.com/v1.0/"
    
    scopes = ['Files.Read', 'Files.Read.All']

    fileDicts= {}
    data = json.loads(request.data)
    folder_dir = data['message'][2]
    flow = data['message'][1]

    app = msal.PublicClientApplication(
        APPLICATION_ID,
    )
    
    fileDicts= {}
    webbrowser.open(flow['verification_uri'])
    result = app.acquire_token_by_device_flow(flow)
    access_token_id = result["access_token"]

    headers = {"Authorization" : "Bearer " + access_token_id}

    # Get all file details in folder
    response_file_info = requests.get(
        base_url + f"/me/drive/root:/{folder_dir}:/children",
        headers=headers
    )
    list_file_response = response_file_info.json()["value"]

    # Map all file id to file name
    for fileDetails in list_file_response:
        print(fileDetails["id"])
        fileDicts[fileDetails["id"]] = fileDetails["name"]

    # Import all files into tempResources folder using their file name
    for fileId in fileDicts:
        response_file_content = requests.get(base_url + f"/me/drive/items/{fileId}/content", 
            headers=headers
        )
        with open(os.path.join(f"{os.getcwd()}/backend/tempResources", fileDicts[fileId]), "wb") as f:
            f.write(response_file_content.content)

    return jsonify({"message" : "Files Successfully Extracted"})


@app.route("/oneDrive", methods=['POST']) # {"message" : "Documents"}
def downloadAll():
    data = json.loads(request.data)
    print(data)
    auth = requests.post("http://127.0.0.1:90/oneDriveAuth", json=data)
    extract_response = requests.post("http://127.0.0.1:90/oneDriveFileExtract", json=auth.json())

    return extract_response.json() #jsonify({"message":[auth1]}) 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=90, debug=True)
