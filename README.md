# Citi Oracle by FinBros

## About
Citi Oracle is a Chat bot utilizing the knowledege graph on neo4j and generative text abilities of OpenAI's API, allowing us to perform powerful queries to produce optimum responses.

The following is the flow of data when a user submits a prompt.<br><br>
<img title="a title" alt="Alt text" src="https://gcdnb.pbrd.co/images/pzBzwGueFMAX.png?o=1">

The unformatted text string is sent to the OpenAi API for formatting, where entities and their relationships are extracted out to from Cypher queries on the neo4j knowledge graph. Once queried, neo4j returns the query result back to OpenAI API in the format of RDF Triples, 
which then formats the data into conversational text for the user to see.


## Getting Started
First, set up the backend by creating the Docker images and containers using docker-compose
```
cd backend
docker compose up
```

Next, run the development server for the frontend
```
cd ../frontend
npm start
```

