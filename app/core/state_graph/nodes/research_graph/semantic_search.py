from core.state_graph.states.research_graph.researcher_state import ResearcherState
from core.prompts import SEMANTIC_SEARCH_SYSTEM_PROMPT
from langchain_core.runnables import RunnableConfig
from typing import TypedDict, cast
from langchain.chat_models import init_chat_model
from core.knowledge_graph.graph import neo4j_graph
from utils.utils import new_uuid
from config import config as app_config
import openai


def execute_semantic_search(node_label: str, attribute_name: str, query: str):
    """Execute a semantic search on Neo4j vector indexes.
    
    This function performs vector-based similarity search using OpenAI embeddings
    to find nodes in the Neo4j graph database that are semantically similar to
    the provided query. It converts the query to an embedding vector and searches
    the corresponding vector index for the most similar nodes.
    
    Args:
        node_label (str): The label of the node type to search (e.g., 'Recipe', 'FoodProduct').
        attribute_name (str): The attribute/property of the node to search within (e.g., 'name', 'description').
        query (str): The search query to find semantically similar content.
        
    Returns:
        list: A list of dictionaries containing the matching nodes with their attributes,
              ordered by similarity score (highest first).
    """
    index_name = f"{node_label.lower()}_{attribute_name}_index"
    top_k = 1
    query_embedding = (
        openai.embeddings.create(model=app_config["embedding_model"], input=query)
        .data[0]
        .embedding
    )

    nodes = (
        f"node.name as name, node.{attribute_name} as {attribute_name}"
        if attribute_name != "name"
        else f"node.{attribute_name} as name"
    )
    response = neo4j_graph.query(
        f"""
        CALL db.index.vector.queryNodes('{index_name}', {top_k}, {query_embedding})
        YIELD node, score
        RETURN {nodes}
        ORDER BY score DESC"""
    )
    print(
        f"Semantic Search Tool invoked with parameters: node_label: '{node_label}', attribute_name: '{attribute_name}', query: '{query}'"
    )
    print(f"Semantic Search response: {response}")
    return response


async def semantic_search(state: ResearcherState, *, config: RunnableConfig):
    """Perform semantic search to find relevant nodes in the research graph.
    
    This function analyzes a research question to determine optimal search parameters
    and executes a semantic search on the Neo4j graph database. It uses an LLM to
    identify which node type and attribute should be searched, then performs vector-based
    similarity search to find semantically related content that can help answer the question.
    
    Args:
        state (ResearcherState): The current researcher state containing the
            research step question and accumulated knowledge.
        config (RunnableConfig): Configuration for the runnable execution.
        
    Returns:
        dict[str, list]: A dictionary with a "knowledge" key containing
            a list with the semantic search results formatted as knowledge items.
    """
    class Response(TypedDict):
        node_label: str
        attribute_name: str
        query: str

    model = init_chat_model(
        name="semantic_search", **app_config["inference_model_params"]
    )

    vector_indexes = neo4j_graph.query("SHOW VECTOR INDEXES YIELD name RETURN name;")
    print(f"vector_indexes: {vector_indexes}")

    system_prompt = SEMANTIC_SEARCH_SYSTEM_PROMPT.format(
        schema=neo4j_graph.get_structured_schema,
        vector_indexes=str(vector_indexes)
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "human", "content": state.step["question"]},
    ]
    response = cast(
        Response, await model.with_structured_output(Response).ainvoke(messages)
    )
    sem_search_response = execute_semantic_search(
        node_label=response["node_label"],
        attribute_name=response["attribute_name"],
        query=response["query"],
    )

    search_names = [f"'{record['name']}'" for record in sem_search_response]
    joined_search_names = ", ".join(search_names)
    knowledge = {
        "id": new_uuid(),
        "content": f"Executed Semantic Search on {response['node_label']}.{response['attribute_name']} for values similar to: '{response['query']}'\nResults: {joined_search_names}",
    }

    return {"knowledge": [knowledge]}
