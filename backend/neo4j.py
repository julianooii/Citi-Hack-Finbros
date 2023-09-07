from flask import Flask, jsonify, request
from spacy.tokens import Doc
import json
import spacy
import subprocess
# from neo4j import GraphDatabase

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm") 
nlp_coref = spacy.load("en_coreference_web_trf")

URI = "neo4j+s://5fb1b60c.databases.neo4j.io"
AUTH = ("neo4j", "n38clRL6k2kfNq00-4i3Z91b1by3JstK4sm6NNP95Dk")

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     driver.verify_connectivity()



@app.route("/processString", methods=["POST"])
def processString():
     # Process whole documents
    data = json.loads(request.data)
    tempDict = {}
    doc_coref = nlp_coref(data["query"])
    input_text = resolve_references(doc_coref)
    print(input_text)
    doc = nlp(input_text) ######## depends on the json input --- to be changed ##############
    # for entity in doc.ents:
    #     label = entity.label_
    #     text = entity.text
    #     if label not in tempDict:
    #         tempDict[label] = [text]
    #     else:
    #         tempDict[label].append(text)
   
    for entity in doc:
        # label = entity.label_
        text = entity.text
        if text not in tempDict:
             tempDict[entity.text] = [entity.text, entity.lemma_, entity.pos_]
             
    cmd = ["java", "-Xmx512m", "-jar", "backend/reverb-latest.jar"]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Pass the input text to the subprocess using stdin.write().
    process.stdin.write(data["query"].encode())
    output, error = process.communicate()
    process.stdin.close()

    if process.returncode == 0:
        extracted_relationships = output.decode()
    
    # Split the extracted relationships into a list, assuming each line represents a relationship.
        relationships_list = extracted_relationships.strip().split('\n')
        # print(relationships_list)
        # Convert the list of relationships into a list of dictionaries.
        relationships = []
        for relationship in relationships_list:
            parts = relationship.split('\t')
            # Assuming the format is: subject, relation, object, confidence
            relationships.append({
                "subject": parts[2],
                "relation": parts[3],
                "object": parts[4],
                "confidence": float(parts[11])
            })

        # Output the relationships as JSON
        output_json = json.dumps(relationships, indent=2)
        return output_json
    else:
        return "Error:" + error.decode()

    
    # return jsonify(
    #     {
    #         "message":"text processed",
    #         "data" : [tempDict]
    #     })


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
            pass



    return

def resolve_references(doc: Doc) -> str:
    """Function for resolving references with the coref ouput
    doc (Doc): The Doc object processed by the coref pipeline
    RETURNS (str): The Doc string with resolved references
    """
    # token.idx : token.text
    token_mention_mapper = {}
    output_string = ""
    clusters = [
        val for key, val in doc.spans.items() if key.startswith("coref_cluster")
    ]

    # Iterate through every found cluster
    for cluster in clusters:
        first_mention = cluster[0]
        # Iterate through every other span in the cluster
        for mention_span in list(cluster)[1:]:
            # Set first_mention as value for the first token in mention_span in the token_mention_mapper
            token_mention_mapper[mention_span[0].idx] = first_mention.text + mention_span[0].whitespace_
            
            for token in mention_span[1:]:
                # Set empty string for all the other tokens in mention_span
                token_mention_mapper[token.idx] = ""

    # Iterate through every token in the Doc
    for token in doc:
        # Check if token exists in token_mention_mapper
        if token.idx in token_mention_mapper:
            output_string += token_mention_mapper[token.idx]
        # Else add original token text
        else:
            output_string += token.text + token.whitespace_

    return output_string

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=90, debug=True)