from flask import Flask, jsonify, request
import json
import spacy
from neo4j import GraphDatabase

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm") 

URI = "neo4j+s://5fb1b60c.databases.neo4j.io"
AUTH = ("neo4j", "n38clRL6k2kfNq00-4i3Z91b1by3JstK4sm6NNP95Dk")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()


@app.route("/processString", methods=["POST"])
def processString():
     # Process whole documents
    data = json.loads(request.data)
    tempDict = {}
    doc = nlp(data) ######## depends on the json input --- to be changed ##############
    for entity in doc.ents:
        label = entity.label_
        text = entity.text
        if label not in tempDict:
            tempDict[label] = [text]
        else:
            tempDict[label].append(text)
    return jsonify(
        {
            "message":"text processed",
            "data" : [tempDict]
        })


@app.route("/updateNodes", methods=["POST"])
def updateNodes():
    data = json.loads(request.data)
    
    DictNodes = data["data"][0] # "ORG" : ["Apple", "Tesla"]
    for node in DictNodes:
        records, summary, keys = driver.execute_query("""
            MATCH (t:Topic {name: $name})
            """, name=node,
            database_="neo4j",
        )
        currentNodes = records.data()
        print(currentNodes) ### to remove

        # If base node doesnt exist, create a new Topic node
        
        if len(currentNodes) == 0:
            summary = driver.execute_query(
                "MERGE (:Person {name: $name})",  
                name="Alice",  
                database_="neo4j",  
            ).summary
        
        # Else if node exists, create a Text node and connect it to existing Topic node
        else:




    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=90, debug=True)