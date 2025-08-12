from core.state_graph.states.research_graph.researcher_state import ResearcherState
from core.prompts import GENERATE_QUERIES_SYSTEM_PROMPT
from core.prompts import FIX_QUERY_SYSTEM_PROMPT
from langchain_core.runnables import RunnableConfig
from typing import TypedDict, cast
from langchain.chat_models import init_chat_model
from core.knowledge_graph.graph import neo4j_graph
from config import config as app_config
from neo4j_graphrag.retrievers.text2cypher import extract_cypher
from langchain_neo4j.chains.graph_qa.cypher_utils import CypherQueryCorrector
from langchain_neo4j.chains.graph_qa.cypher_utils import Schema


async def correct_query_by_llm(query: str) -> str:
    model = init_chat_model(
        name="correct_query_by_llm", **app_config["inference_model_params"]
    )
    system_prompt = FIX_QUERY_SYSTEM_PROMPT.format(
        schema=neo4j_graph.get_structured_schema
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "human", "content": query},
    ]
    response = await model.ainvoke(messages)
    # print(f"Query before LLM correction: {query}")
    # print(f"Query after LLM correction: {response.content}")
    return response.content


def correct_query_by_parser(query: str) -> str:
    corrector_schema = [
        Schema(el["start"], el["type"], el["end"])
        for el in neo4j_graph.get_structured_schema.get("relationships", [])
    ]
    cypher_query_corrector = CypherQueryCorrector(corrector_schema)

    extracted_query = extract_cypher(text=query)
    corrected_query = cypher_query_corrector(extracted_query)

    # print(f"Query before parser correction: {query}")
    # print(f"Query after parser correction: {corrected_query}")
    return corrected_query


async def generate_queries(
    state: ResearcherState, *, config: RunnableConfig
) -> dict[str, list[str]]:
    
    class Response(TypedDict):
        queries: list[str]

    print("---GENERATE QUERIES---")
    formatted_knowledge = "\n\n".join(
        [f"{i+1}. {item['content']}" for i, item in enumerate(state.knowledge)]
    )
    model = init_chat_model(
        name="generate_queries", **app_config["inference_model_params"]
    )
    system_prompt = GENERATE_QUERIES_SYSTEM_PROMPT.format(
        schema=neo4j_graph.get_schema, context=formatted_knowledge
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "human", "content": state.step["question"]},
    ]
    response = cast(
        Response, await model.with_structured_output(Response).ainvoke(messages)
    )
    response["queries"] = [
        await correct_query_by_llm(query=q) for q in response["queries"]
    ]
    response["queries"] = [
        correct_query_by_parser(query=q) for q in response["queries"]
    ]

    print(f"Queries: {response['queries']}")
    return {"queries": response["queries"]}
