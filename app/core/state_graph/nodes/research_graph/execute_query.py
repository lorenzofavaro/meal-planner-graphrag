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
