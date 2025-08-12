from dataclasses import dataclass, field
from typing import Annotated
from utils.utils import update_knowledge
from core.state_graph.states.main_graph.input_state import InputState
from core.state_graph.states.main_graph.router import Router
from core.state_graph.states.step import Step


@dataclass(kw_only=True)
class AgentState(InputState):
    router: Router = field(default_factory=lambda: Router(type="general", logic=""))
    steps: list[Step] = field(default_factory=list)
    knowledge: Annotated[list[dict], update_knowledge] = field(default_factory=list)
