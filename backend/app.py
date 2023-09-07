from __future__ import print_function
import json
from pymongo import MongoClient
from flask import Flask, jsonify, request
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
# install this package
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import shutil
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

@app.route("/gdrive", methods=["POST"])
def gdrive():
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.readonly']
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # full link --> https://drive.google.com/drive/folders/1DdXx-CfRzcSCYAjCPQVV29wfxkW_yD1g?usp=drive_link
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(q=f"'1DdXx-CfRzcSCYAjCPQVV29wfxkW_yD1g' in parents",
                                   pageSize=20, fields="nextPageToken, files(id, name)",).execute()
    items = results.get('files', [])

    for id_url in items:
        file_id = id_url['id']
        results = service.files().get(fileId=file_id).execute()
        name = results['name']
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        fh.seek(0)
        # Write the received data to the file
        path = "/Users/alden/Documents/GitHub/Citi-Hack-Finbros/downloaded_files/" + name
        with open(path, 'wb') as f:
            shutil.copyfileobj(fh, f)


@app.route("/oneDriveAuth", methods=['POST'])
def MicrosoftAuth():
    tenent_id = "55dd5550-5d6b-43fd-99c3-caa837fa27dc"
    APPLICATION_ID = "27f17a4b-5e7e-477e-866f-6eff3e3aa049"
    CLIENT_SECRET = "Bx~8Q~lpYniXgL6vuD56dxLR4UDRAxZ5ZGLpMcua"
    base_url = "https://graph.microsoft.com/v1.0/"
    
    authority_url = 'https://login.microsoft.com/consumers/'
    scopes = ['Files.Read', 'Files.Read.All']

    fileDicts= {}
    data = json.loads(request.data)
    folder_dir = data['message']

    app = msal.PublicClientApplication(
        APPLICATION_ID,
    )
    flow = app.initiate_device_flow(scopes=scopes)
    print(flow['message'])
    print(flow['message'].split()[-3])

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
