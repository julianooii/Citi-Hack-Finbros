from neo4j import GraphDatabase
URI = "neo4j+s://5fb1b60c.databases.neo4j.io"
AUTH = ("neo4j", "n38clRL6k2kfNq00-4i3Z91b1by3JstK4sm6NNP95Dk")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    
