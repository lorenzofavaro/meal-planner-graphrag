from core.state_graph.states.main_graph.agent_state import AgentState
from core.prompts import MORE_INFO_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage
from config import config as app_config


async def ask_for_more_info(
    state: AgentState, *, config: RunnableConfig
) -> dict[str, list[BaseMessage]]:
    """
    Asks the user for more information based on the current routing logic.

    Args:
        state (AgentState): The current state of the agent, including routing logic and messages.
        config (RunnableConfig): Configuration for the runnable execution.

    Returns:
        dict[str, list[BaseMessage]]: A dictionary containing the new message(s) requesting more information.
    """
    model = init_chat_model(
        name="ask_for_more_info", **app_config["inference_model_params"]
    )
    system_prompt = MORE_INFO_SYSTEM_PROMPT.format(logic=state.router.logic)
    messages = [{"role": "system", "content": system_prompt}] + state.messages
    response = await model.ainvoke(messages)
    return {"messages": [response]}
