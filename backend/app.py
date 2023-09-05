import json
from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


def get_db():
    client = MongoClient(host = 'mongodb',
                         port = 27017)
    
    db = client["citi_finbros_db"]
    return db

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
