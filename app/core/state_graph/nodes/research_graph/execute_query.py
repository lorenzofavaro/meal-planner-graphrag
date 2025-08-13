from core.state_graph.states.research_graph.query_state import QueryState
from langchain_core.runnables import RunnableConfig
from core.knowledge_graph.graph import neo4j_graph
from utils.utils import new_uuid


def remove_embedding_keys(obj):
    if isinstance(obj, dict):
        return {
            k: remove_embedding_keys(v)
            for k, v in obj.items()
            if "embedding" not in k.lower()
        }
    elif isinstance(obj, list):
        return [remove_embedding_keys(item) for item in obj]
    else:
        return obj


async def execute_query(state: QueryState, *, config: RunnableConfig):
    """
    Execute a query against the Neo4j knowledge graph and format the results.
    
    This function takes a Cypher query from the state, executes it against the Neo4j
    graph database, and returns the top results with embedding keys removed for cleaner
    output. The results are formatted as knowledge entries that can be used by other
    nodes in the research graph.
    
    Args:
        state (QueryState): The current state containing the query to execute
        config (RunnableConfig): Configuration for the runnable execution
        
    Returns:
        dict: A dictionary containing a list of knowledge entries with the query results
    """
    # print(f"Query for the retrieval process: {state.query}")
    top_k = 10
    response = neo4j_graph.query(state.query)[:top_k]
    cleaned_response = remove_embedding_keys(response)

    pairs = [
        ", ".join(f"{k}: {v}" for k, v in record.items()) for record in cleaned_response
    ]
    knowledge = {
        "id": new_uuid(),
        "content": f"Executed Query Search with the following query: '{state.query}'\Response:\n\t"
        + "\n\t".join(pairs),
    }

    # print(f"New knowledge: {knowledge}")
    return {"knowledge": [knowledge]}
