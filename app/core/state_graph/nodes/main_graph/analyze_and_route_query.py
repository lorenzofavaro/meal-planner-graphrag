from core.state_graph.states.main_graph.agent_state import AgentState
from core.state_graph.states.main_graph.router import Router
from core.prompts import ROUTER_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from typing import cast
from config import config as app_config


async def analyze_and_route_query(
    state: AgentState, *, config: RunnableConfig
) -> dict[str, Router]:
    model = init_chat_model(
        name="analyze_and_route_query", **app_config["inference_model_params"]
    )
    messages = [{"role": "system", "content": ROUTER_SYSTEM_PROMPT}] + state.messages
    print("---ANALYZE AND ROUTE QUERY---")
    print(f"MESSAGES: {state.messages}")
    response = cast(
        Router, await model.with_structured_output(Router).ainvoke(messages)
    )
    return {"router": response}
