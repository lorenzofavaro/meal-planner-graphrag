import uuid
from typing import Literal, Optional, Union


def new_uuid():
    return str(uuid.uuid4())


def update_knowledge(
    existing: Optional[list[dict]], new: Union[list[dict], Literal["delete"]]
) -> list[dict]:
    if new == "delete":
        return []

    ids = set([item["id"] for item in existing])
    for item in new:
        if item["id"] not in ids:
            existing.append(item)
    return existing
