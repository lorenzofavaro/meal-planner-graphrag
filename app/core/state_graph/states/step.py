from typing import TypedDict
from typing import Literal


class Step(TypedDict):
    question: str
    type: Literal["semantic_search", "query_search"]
