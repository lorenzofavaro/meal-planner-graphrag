from langgraph.graph import END, START, StateGraph
from core.state_graph.states.main_graph.agent_state import AgentState
from core.state_graph.states.main_graph.input_state import InputState
from core.state_graph.nodes.main_graph.analyze_and_route_query import (
    analyze_and_route_query,
)
from core.state_graph.nodes.main_graph.route_query import route_query
from core.state_graph.nodes.main_graph.ask_for_more_info import ask_for_more_info
from core.state_graph.nodes.main_graph.respond_to_general_query import (
    respond_to_general_query,
)
from core.state_graph.nodes.main_graph.create_research_plan import create_research_plan
from core.state_graph.nodes.main_graph.conduct_research import conduct_research
from core.state_graph.nodes.main_graph.respond import respond
from core.state_graph.nodes.main_graph.check_finished import check_finished


def build_main_graph():
    builder = StateGraph(AgentState, input=InputState)
    builder.add_node(analyze_and_route_query)
    builder.add_node(ask_for_more_info)
    builder.add_node(respond_to_general_query)
    builder.add_node(create_research_plan)
    builder.add_node(conduct_research)
    builder.add_node("respond", respond)

    builder.add_edge("create_research_plan", "conduct_research")
    builder.add_edge(START, "analyze_and_route_query")
    builder.add_conditional_edges("analyze_and_route_query", route_query)
    builder.add_conditional_edges("conduct_research", check_finished)
    builder.add_edge("respond", END)

    return builder.compile()
