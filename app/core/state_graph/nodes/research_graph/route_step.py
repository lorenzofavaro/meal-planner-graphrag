from core.state_graph.states.research_graph.researcher_state import ResearcherState
from typing import Literal


def route_step(
    state: ResearcherState,
) -> Literal["generate_queries", "semantic_search"]:
    _type = state.step["type"]
    if _type == "semantic_search":
        return "semantic_search"
    elif _type == "query_search":
        return "generate_queries"
    else:
        raise ValueError(f"Unknown router type {_type}")
