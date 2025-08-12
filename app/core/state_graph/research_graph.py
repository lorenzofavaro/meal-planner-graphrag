from langgraph.graph import END, START, StateGraph
from core.state_graph.states.research_graph.researcher_state import ResearcherState
from core.state_graph.nodes.research_graph.generate_queries import generate_queries
from core.state_graph.nodes.research_graph.execute_query import execute_query
from core.state_graph.nodes.research_graph.semantic_search import semantic_search
from core.state_graph.nodes.research_graph.route_step import route_step
from core.state_graph.nodes.research_graph.query_in_parallel import query_in_parallel


def build_research_graph():
    builder = StateGraph(ResearcherState)
    builder.add_node(generate_queries)
    builder.add_node(execute_query)
    builder.add_node(semantic_search)

    builder.add_conditional_edges(
        START,
        route_step,
        {"generate_queries": "generate_queries", "semantic_search": "semantic_search"},
    )
    builder.add_conditional_edges(
        "generate_queries",
        query_in_parallel,  # type: ignore
        path_map=["execute_query"],
    )
    builder.add_edge("execute_query", END)
    builder.add_edge("semantic_search", END)

    return builder.compile()


research_graph = build_research_graph()
