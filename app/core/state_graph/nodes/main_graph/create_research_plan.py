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
    """
    Reviews a research plan to ensure its quality and relevance.

    Args:
        plan (Plan): The research plan to be reviewed.

    Returns:
        Plan: The reviewed and potentially modified research plan.
    """
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
    """
    Reduces a research plan by simplifying or condensing its steps.

    Args:
        plan (Plan): The research plan to be reduced.

    Returns:
        Plan: The reduced research plan.
    """
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
    """
    Creates, reduces, and reviews a research plan based on the agent's current knowledge and messages.

    Args:
        state (AgentState): The current state of the agent, including knowledge and messages.
        config (RunnableConfig): Configuration for the runnable execution.

    Returns:
        dict[str, list[str] | str]: A dictionary containing the final steps of the reviewed plan and an empty knowledge list.
    """
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
