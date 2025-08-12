from core.state_graph.states.research_graph.researcher_state import ResearcherState
from core.state_graph.states.research_graph.query_state import QueryState
from langgraph.types import Send


def query_in_parallel(state: ResearcherState) -> list[Send]:
    return [Send("execute_query", QueryState(query=query)) for query in state.queries]
