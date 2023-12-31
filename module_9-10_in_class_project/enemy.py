"""Represent an enemy in our game."""

from __future__ import annotations

import item
import being
import map_cell

class Enemy(being.Being):
    """Represent an enemy in our game."""
    def __init__(self,
                 id: int=0,
                 name: str="unnamed enemy",
                 description: str="undescribed enemy",
                 stats: dict[str, int]={"attack":0, "defence": 0, "speed": 0, "health": 0},
                 equipment: dict[str, item.Item] | None=None,
                 inventory: list[item.Item] | None=None,
                 location: map_cell.MapCell | None=None
                 ) -> None:
        super().__init__(id, name, description, stats, equipment, inventory, location)
