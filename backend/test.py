from neo4j import GraphDatabase
URI = "neo4j+s://5fb1b60c.databases.neo4j.io"
AUTH = ("neo4j", "n38clRL6k2kfNq00-4i3Z91b1by3JstK4sm6NNP95Dk")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    # records, summary, keys = driver.execute_query (
    #     "MATCH (n:City) RETURN n LIMIT 25",
    #     parameters=None,
    #     db="neo4j",
    # )
    # print("Records:", records)
    # print("Summary:", summary)
    # print("Keys:", keys)

    # records, summary, keys = driver.execute_query (
    #     """
    #         MATCH p=()-[r:IN]->()
    #         RETURN
    #         p AS path,
    #         STARTNODE(r) AS startNode,
    #         ENDNODE(r) AS endNode
    #         LIMIT 25
    #     """,
    #     parameters=None,
    #     db="neo4j",
        
    # )
    def run_query(uri, username, password, query):
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            with driver.session() as session:
                result = session.run(query)
                records = list(result)
                return records
    
    def extract_relationship_type(cypher_query):
        # Split the query by spaces to analyze each word/token
        query_tokens = cypher_query.split()

        # Iterate through the tokens to find the relationship type
        for i, token in enumerate(query_tokens):
            if token.upper() == "MATCH" and i < len(query_tokens) - 1:
                next_token = query_tokens[i + 1].strip("()").strip("-")
                next_token = next_token.split(":")[1].strip("-")
                next_token = next_token.split("]")[0].strip("-")
                if next_token:
                    return next_token

        # Return None if no relationship type is found
        return None
    
    cypher_query = """
            MATCH p=()-[r:IN]->()
            RETURN
            p AS path,
            STARTNODE(r) AS startNode,
            ENDNODE(r) AS endNode
            LIMIT 25
        """
    query_result = run_query(URI, AUTH[0], AUTH[1], cypher_query)

    for record in query_result:
        path = record["path"]
        start_node = record["startNode"]
        end_node = record["endNode"]
        print(start_node['name'], extract_relationship_type(cypher_query), end_node['name'])
    


