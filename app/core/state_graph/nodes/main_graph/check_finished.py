from core.state_graph.states.main_graph.agent_state import AgentState
from typing import Literal


def check_finished(state: AgentState) -> Literal["respond", "conduct_research"]:
    if len(state.steps or []) > 0:
        return "conduct_research"
    else:
        return "respond"
