from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from gradio import EventData


@dataclass
class EntitySelection:
    """
    Selected an entity, or an instance of an entity.

    If the entity was selected within a view, then this also
    includes the view's name.

    If the entity was selected within a 2D or 3D space view,
    then this also includes the position.
    """

    @property
    def kind(self) -> Literal["entity"]:
        return "entity"

    entity_path: str
    instance_id: int | None
    view_name: str | None
    position: tuple[int, int, int] | None


@dataclass
class ViewSelection:
    """Selected a view."""

    @property
    def kind(self) -> Literal["view"]:
        return "view"

    view_id: str
    view_name: str


@dataclass
class ContainerSelection:
    """Selected a container."""

    @property
    def kind(self) -> Literal["container"]:
        return "container"

    container_id: str
    container_name: str


SelectionItem = EntitySelection | ViewSelection | ContainerSelection
"""A single item in a selection."""


def _selection_item_from_json(json: Any) -> SelectionItem:
    if json["type"] == "entity":
        position = json.get("position", None)
        return EntitySelection(
            entity_path=json["entity_path"],
            instance_id=json.get("instance_id", None),
            view_name=json.get("view_name", None),
            position=(position[0], position[1], position[2]) if position is not None else None,
        )
    if json["type"] == "view":
        return ViewSelection(view_id=json["view_id"], view_name=json["view_name"])
    if json["type"] == "container":
        return ContainerSelection(container_id=json["container_id"], container_name=json["container_name"])
    else:
        raise NotImplementedError(f"selection item kind {json[type]} is not handled")


class SelectionChange(EventData):
    def __init__(self, target: Any, data: Any):
        super().__init__(target, data)

        self.items: list[SelectionItem] = [
            _selection_item_from_json(item) for item in data
        ]


class TimeUpdate(EventData):
    def __init__(self, target: Any, data: Any):
        super().__init__(target, data)

        self.time = data

class TimelineChange(EventData):
    def __init__(self, target: Any, data: Any):
        super().__init__(target, data)

        self.timeline = data["timeline"]
        self.time = data["time"]


