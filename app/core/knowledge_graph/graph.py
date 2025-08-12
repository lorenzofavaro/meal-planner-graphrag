import os
from langchain_neo4j import Neo4jGraph


def init_neo4j_graph():
    neo4j_url = os.getenv("NEO4J_URL")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    return Neo4jGraph(
        url=neo4j_url,
        username=neo4j_username,
        password=neo4j_password,
        enhanced_schema=True,
    )


neo4j_graph = init_neo4j_graph()
