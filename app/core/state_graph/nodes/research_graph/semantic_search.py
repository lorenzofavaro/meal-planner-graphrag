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

    # print(f"New knowledge: {knowledge}")
    return {"knowledge": [knowledge]}
