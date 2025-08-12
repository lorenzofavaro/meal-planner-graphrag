from dataclasses import dataclass
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


@dataclass(kw_only=True)
class InputState:
    messages: Annotated[list[AnyMessage], add_messages]
