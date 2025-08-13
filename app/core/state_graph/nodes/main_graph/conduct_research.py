from core.state_graph.states.main_graph.agent_state import AgentState
from core.state_graph.research_graph import research_graph
from typing import Any


async def conduct_research(state: AgentState) -> dict[str, Any]:
    """
    Executes a research step using the research graph and updates the agent's knowledge.

    Args:
        state (AgentState): The current state of the agent, including steps and knowledge.

    Returns:
        dict[str, Any]: A dictionary containing the updated knowledge and remaining steps.
    """
    response = await research_graph.ainvoke(
        {"step": state.steps[0], "knowledge": state.knowledge}
    )  # graph call directly
    knowledge = response["knowledge"]
    step = state.steps[0]
    print(
        f"\n{len(knowledge)} pieces of knowledge retrieved in total for the step: {step}."
    )
    return {"knowledge": knowledge, "steps": state.steps[1:]}
