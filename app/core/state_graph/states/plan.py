from typing import TypedDict
from core.state_graph.states.step import Step


class Plan(TypedDict):
    steps: list[Step]
