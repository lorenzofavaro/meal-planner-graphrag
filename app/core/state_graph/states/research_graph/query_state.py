from dataclasses import dataclass


@dataclass(kw_only=True)
class QueryState:
    query: str
