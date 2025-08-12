import chainlit as cl
from core.state_graph.states.main_graph.input_state import InputState
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from core.state_graph.states.main_graph.router import Router
from config import config
import re


@cl.step(type="tool", name="Message Length Check", show_input=False)
async def message_length_step():
    return f"The input was truncated to {config['max_query_length']} characters."


@cl.step(type="llm", name="Create Research Plan", show_input=False)
async def research_plan_step(plan: dict):
    current_step = cl.context.current_step
    for i, step in enumerate(plan["steps"]):
        await current_step.stream_token(
            f"{i+1}. **{step['type']}**: {step['question']}\n"
        )


@cl.step(type="llm", name="Classify Request", show_input=False)
async def classification_step(classification: Router):
    current_step = cl.context.current_step
    await current_step.stream_token(
        f"Classified as **{classification.type}** with the logic: _{classification.logic}_"
    )


@cl.step(type="llm", name="Generate Query", show_input=False)
async def generate_query_step(query: str):
    current_step = cl.context.current_step

    query = re.sub(r"^cypher[\s\n]*", "", query, flags=re.IGNORECASE)
    query = f"```cypher\n{query.strip()}\n```"
    await current_step.stream_token(query)


async def execute(message: cl.Message):
    graph: Runnable = cl.user_session.get("graph")
    state: InputState = cl.user_session.get("state")

    # Verify query length
    question = message.content
    if len(message.content) > config["max_query_length"]:
        question = message.content[: config["max_query_length"]]
        await message_length_step()

    # Append the new user message to the state
    state.messages += [HumanMessage(content=question)]

    # Stream the response to the UI
    ui_message = cl.Message(content="")
    await ui_message.send()
    async for event in graph.astream_events(state, version="v1"):
        if event["name"] == "create_research_plan" and event["event"] == "on_chain_end":
            steps = event["data"]["output"]
            await research_plan_step(steps)
        elif (
            event["name"] == "analyze_and_route_query"
            and event["event"] == "on_chain_end"
        ):
            classification = event["data"]["output"]["router"]
            await classification_step(classification)
        elif (
            event["name"] == "correct_query_by_llm"
            and event["event"] == "on_chat_model_end"
        ):
            query = event["data"]["output"]["generations"][0][0]["text"]
            await generate_query_step(query)
        elif (
            event["name"]
            in {"ask_for_more_info", "respond_to_general_query", "respond"}
            and event["event"] == "on_chat_model_stream"
        ):
            content = event["data"]["chunk"].content or ""
            await ui_message.stream_token(token=content)
    await ui_message.update()

    # Append the new AI message to the state
    state.messages += [AIMessage(content=ui_message.content)]
