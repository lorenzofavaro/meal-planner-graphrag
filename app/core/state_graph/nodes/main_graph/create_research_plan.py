from core.state_graph.states.main_graph.agent_state import AgentState
from core.state_graph.states.plan import Plan
from core.prompts import RESEARCH_PLAN_SYSTEM_PROMPT
from core.prompts import REDUCE_RESEARCH_PLAN_SYSTEM_PROMPT
from core.prompts import REVIEW_RESEARCH_PLAN_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from typing import cast
from core.knowledge_graph.graph import neo4j_graph
from config import config as app_config


async def review_research_plan(plan: Plan) -> Plan:
    formatted_plan = ""
    for i, step in enumerate(plan["steps"]):
        formatted_plan += f"{i+1}. ({step['type']}): {step['question']}\n"

    model = init_chat_model(
        name="create_research_plan", **app_config["inference_model_params"]
    )
    system_prompt = REVIEW_RESEARCH_PLAN_SYSTEM_PROMPT.format(
        schema=neo4j_graph.get_structured_schema, plan=formatted_plan
    )

    reviewed_plan = cast(
        Plan, await model.with_structured_output(Plan).ainvoke(system_prompt)
    )
    return reviewed_plan


async def reduce_research_plan(plan: Plan) -> Plan:
    formatted_plan = ""
    for i, step in enumerate(plan["steps"]):
        formatted_plan += f"{i+1}. ({step['type']}): {step['question']}\n"

    model = init_chat_model(
        name="reduce_research_plan", **app_config["inference_model_params"]
    )
    system_prompt = REDUCE_RESEARCH_PLAN_SYSTEM_PROMPT.format(
        schema=neo4j_graph.get_structured_schema, plan=formatted_plan
    )

    reduced_plan = cast(
        Plan, await model.with_structured_output(Plan).ainvoke(system_prompt)
    )
    return reduced_plan


async def create_research_plan(
    state: AgentState, *, config: RunnableConfig
) -> dict[str, list[str] | str]:
    formatted_knowledge = "\n".join([item["content"] for item in state.knowledge])
    model = init_chat_model(
        name="create_research_plan", **app_config["inference_model_params"]
    )
    system_prompt = RESEARCH_PLAN_SYSTEM_PROMPT.format(
        schema=neo4j_graph.get_structured_schema, context=formatted_knowledge
    )
    messages = [{"role": "system", "content": system_prompt}] + state.messages
    print("---PLAN GENERATION---")

    # Generate plan
    plan = cast(Plan, await model.with_structured_output(Plan).ainvoke(messages))
    print("Plan")
    for i, step in enumerate(plan["steps"]):
        print(f"{i+1}. ({step['type']}): {step['question']}")

    # Reduce plan
    reduced_plan = cast(Plan, await reduce_research_plan(plan=plan))
    print("Reduced Plan")
    for i, step in enumerate(reduced_plan["steps"]):
        print(f"{i+1}. ({step['type']}): {step['question']}")

    # Review plan
    reviewed_plan = cast(Plan, await review_research_plan(plan=reduced_plan))

    print("Reviewed Plan")
    for i, step in enumerate(reviewed_plan["steps"]):
        print(f"{i+1}. ({step['type']}): {step['question']}")

    return {"steps": reviewed_plan["steps"], "knowledge": []}
