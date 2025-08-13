from core.state_graph.states.research_graph.researcher_state import ResearcherState
from typing import Literal


def route_step(
    state: ResearcherState,
) -> Literal["generate_queries", "semantic_search"]:
    """
    Route the research step to the appropriate execution node based on step type.
    
    This function examines the step type in the researcher state and determines
    which node should handle the next step of the research process. It supports
    two types of research steps: semantic search and query-based search.
    
    Args:
        state (ResearcherState): The current researcher state containing the step
                                information with a "type" field
    
    Returns:
        Literal["generate_queries", "semantic_search"]: The name of the next node
            to execute:
            - "semantic_search" for semantic search steps
            - "generate_queries" for query-based search steps
    
    Raises:
        ValueError: If the step type is not recognized (not "semantic_search" 
                   or "query_search")
    """
    _type = state.step["type"]
    if _type == "semantic_search":
        return "semantic_search"
    elif _type == "query_search":
        return "generate_queries"
    else:
        raise ValueError(f"Unknown router type {_type}")
