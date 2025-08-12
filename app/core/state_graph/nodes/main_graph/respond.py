from core.state_graph.states.main_graph.agent_state import AgentState
from core.prompts import RESPONSE_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage
from config import config as app_config


async def respond(
    state: AgentState, *, config: RunnableConfig
) -> dict[str, list[BaseMessage]]:
    print("--- RESPONSE GENERATION STEP ---")
    model = init_chat_model(name="respond", **app_config["inference_model_params"])
    formatted_knowledge = "\n\n".join([item["content"] for item in state.knowledge])
    prompt = RESPONSE_SYSTEM_PROMPT.format(context=formatted_knowledge)
    messages = [{"role": "system", "content": prompt}] + state.messages
    response = await model.ainvoke(messages)

    return {"messages": [response]}
