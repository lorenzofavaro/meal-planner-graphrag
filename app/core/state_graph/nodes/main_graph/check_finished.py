from core.state_graph.states.main_graph.agent_state import AgentState
from typing import Literal


def check_finished(state: AgentState) -> Literal["respond", "conduct_research"]:
    """
    Determines whether the agent should respond or conduct further research based on the steps taken.

    Args:
        state (AgentState): The current state of the agent, including the steps performed.

    Returns:
        Literal["respond", "conduct_research"]: 
            "conduct_research" if there are steps present, otherwise "respond".
    """
    if len(state.steps or []) > 0:
        return "conduct_research"
    else:
        return "respond"
