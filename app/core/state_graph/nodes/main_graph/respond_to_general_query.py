from core.state_graph.states.main_graph.agent_state import AgentState
from core.prompts import GENERAL_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage
from config import config as app_config


async def respond_to_general_query(
    state: AgentState, *, config: RunnableConfig
) -> dict[str, list[BaseMessage]]:
    model = init_chat_model(
        name="respond_to_general_query", **app_config["inference_model_params"]
    )
    system_prompt = GENERAL_SYSTEM_PROMPT.format(logic=state.router.logic)
    print("---RESPONSE GENERATION---")
    messages = [{"role": "system", "content": system_prompt}] + state.messages
    response = await model.ainvoke(messages)
    return {"messages": [response]}
