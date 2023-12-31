"""Represents the abstract similarities among beings, items, maps, and other game entities."""

from __future__ import annotations

import item
# import map_cell # import map_cell causes circular import, even though it is only used for type hints

class Entity:
    """An "abstract" class that contains common attributes among different game entities."""

    def __init__(self,
                 id: int=0,
                 name: str="unnamed entity",
                 description: str="undescribed entity",
                 stats: dict[str, int]={},
                 equipment: dict[str, item.Item] | None=None,
                 inventory: list[item.Item] | None=None,
                 location=None # None represents an object existing in the game but not yet being placed in the game
                 ) -> None:
        """Initialize this "object", likely only used to set base values for subclasses."""
        self.id: int = id
        self.name: str = name
        self.description: str = description
        # maybe we should make a stats class to handle complex issues with stat representation....
        self.valid_stats: list[str] = ["attack", "defence", "speed", "health", "experience"]
        self.stats: dict[str, int] = {}
        
        # set all default stats to 0 if not otherwise given
        for stat in self.valid_stats:
            self.stats[stat] = 0
        for stat_name,stat in stats.items():
            if stat_name in self.valid_stats:
                self.stats[stat_name] = stat
            else:
                print(f"{name} has a stat ({stat_name}) that is not listed in the valid stats for this entity, did you mean to create it first?\n\t valid stats are: {self.valid_stats}")

        if equipment is None:
            self.equipment: dict[str, item.Item] = {}
        else:
            self.equipment: dict[str, item.Item] = equipment # for upgrades on the equipment

        if inventory is None:
            self.inventory: list[item.Item] = []
        else:
            self.inventory: list[item.Item] = inventory # if this item has an inventory...

        self.location = location

    def __str__(self, additional_attributes_categorical_names: list[str | None] | None=None, additional_attributes_list: list[list[tuple[str | None, str | None]]] | None=None) -> str:
        """Human readable formatted data of this object.
        
            @param: additional_attributes_categorical_names is a list of categorical names to be printed before the associated list of additional attributes
            @param: additional_attributes_list is a dictionary where keys are the name of an attribute to be added and the values are the value associated with that added attribute.
        """
        result: str =  f"Name: {self.name}:\n"
        if self.location is not None:
            result += f"\tlocation: {self.location.name}\n"
        else:
            result += f"\tlocation: nowhere...\n"
        result += f"\tDescription: {self.description}\n"
        
        # if no additional attributes, then do not print anything else
        if additional_attributes_list is not None:
            # if categorical names exist, then use them with the additional attributes lists
            additional_attributes_tab_level: str = "\t"
            if additional_attributes_categorical_names is not None:
                for count in range(len(additional_attributes_list)):
                    if count < len(additional_attributes_categorical_names):
                        additional_attributes_categorical_name: str | None = additional_attributes_categorical_names[count]
                    else:
                        additional_attributes_categorical_name = None
                    additional_attributes: list[tuple[str | None, str | None]] = additional_attributes_list[count]
                    # reset, as each list might or might not have a categorical name
                    additional_attributes_tab_level = "\t"
                    # if categorical name is not none, then increase tab level to nest under categorical name
                    if additional_attributes_categorical_name is not None:
                        result += f"{additional_attributes_tab_level}{additional_attributes_categorical_name}:\n"
                        # increase tab level if we have a categorical name
                        additional_attributes_tab_level += "\t"
                    if additional_attributes is not None:
                        for attribute_name, attribute_value in additional_attributes:
                            result += f"{additional_attributes_tab_level}"
                            if attribute_name is not None:
                                result += f"{attribute_name}: "
                            if attribute_value is not None:
                                result += f"{attribute_value}\n"
            # otherwise, just print all additional attributes one level under character
            else:
                for additional_attributes in additional_attributes_list:
                    for attribute_name, attribute_value in additional_attributes:
                            result += f"{additional_attributes_tab_level}{attribute_name}: {attribute_value}\n"
        
        # check for any stat that is non-zero, otherwise do not even display the line for stats categorical name
        non_zero_stat: bool = False
        for stat in self.stats.values():
            if stat > 0:
                non_zero_stat = True
                break

        # only print stats string if at least one stat is non-zero and implicitly stats having a length
        if len(self.stats) > 0 and non_zero_stat:
            result += f"\tStats:\n"
            for stat_name,stat in self.stats.items():
                if stat > 0:
                    result += f"\t\t{stat_name}: {stat}\n"
        
        if len(self.equipment) > 0:
            result += f"\tEquipment:\n"
            result += f"_____________begin of equipment for {self.name}________________\n"
            for equip_slot, equipped_item in self.equipment.items():
                if equipped_item is not None:
                    result += f"{equip_slot}: {equipped_item.name} ("
                    for stat_name, stat_value in equipped_item.stats.items():
                        result += f"{stat_name}: {stat_value}, "
                    result = result[:-2] + ")\n" # hack to remove last comma!
                else:
                    print("that equipped item is None...?")
            result += f"_____________end of equipment for {self.name}________________\n"
        
        if len(self.inventory) > 0:
            result += f"\tInventory:\n"
            result += f"_____________begin of inventory of {self.name}________________\n"
            for element in self.inventory:
                result += f"{element}\n"
            result += f"_____________end of inventory of {self.name}________________\n"

        return result
    
    def add_item(self, proposed_item: item.Item | None=None) -> str:
        """Add item to this Entity's inventory if it is not None."""
        result: str = ""
        if proposed_item is not None:
            self.inventory.append(proposed_item)
            result += f"{proposed_item.name} has been added to {self.name}'s inventory."
        else:
            result += "that item is None, did you forget to pass an actual object into the add_item method?"
        
        return result
    
    def remove_item(self, proposed_item: item.Item | None=None) -> str:
        """Remove item from this Entity's inventory if it is not None."""
        result: str = ""
        if proposed_item is not None:
            # find item in inventory if it is indeed in there
            found_item: item.Item | None = None
            for index,current_item in enumerate(self.inventory):
                if current_item.id == proposed_item.id:
                    found_item = self.inventory.pop(index)
            if found_item is not None:
                result += f"{proposed_item.name} has been removed from {self.name}'s inventory."
            else:
                result += f"{proposed_item.name} was not found in {self.name}'s inventory."
        else:
            result += "that item is None, did you forget to pass an actual object into the remove_item method?"
        
        return result
    
    def equip(self, item_proposed: item.Item | None=None):
        """Attempt to equip item on this entity, taking into account equipment slots..."""
        result: str = ""
        if item_proposed is not None:
            if item_proposed.is_equipped is False:
                # check if that slot is already in use, if so, unequip that item first!
                if item_proposed.is_equippable is True and item_proposed.equipment_slot is not None:
                    # check equipped items for unequipment only if that slot is already in use (not None)
                    if item_proposed.equipment_slot in self.equipment:
                        current_equip: item.Item | None = self.equipment[item_proposed.equipment_slot]
                        if current_equip is not None:
                            # unequip old item and reduce stats first!
                            del self.equipment[item_proposed.equipment_slot]
                            current_equip.is_equipped = False
                            for item_stat_name,item_stat in current_equip.stats.items():
                                self.stats[item_stat_name] -= item_stat
                    # actually label as equipped and add stats
                    self.equipment[item_proposed.equipment_slot] = item_proposed
                    item_proposed.is_equipped = True
                    for item_stat_name,item_stat in item_proposed.stats.items():
                        if item_stat_name in self.stats:
                            self.stats[item_stat_name] += item_stat
                        else:
                            self.stats[item_stat_name] = item_stat
                else:
                    result = f"{item_proposed.name}({item_proposed.equipment_slot}) is not equippable"
            else:
                result = f"{item_proposed.name} is already equipped, did you mean to unequip it?"
        else:
            result = "That item is None, you cannot equip it, did you forget to pass an actual item to the equip method?"

        return result
    
    def unequip(self, item_proposed: item.Item | None=None):
        """Attempt to unequip item on this entity."""
        result: str = ""
        if item_proposed is not None:
            if item_proposed.is_equipped is True:
                if item_proposed.equipment_slot in self.equipment:
                    current_equip: item.Item | None = self.equipment[item_proposed.equipment_slot]
                    if current_equip is not None:
                        # unequip old item and reduce stats!
                        del self.equipment[item_proposed.equipment_slot]
                        current_equip.is_equipped = False
                        for item_stat_name,item_stat in current_equip.stats.items():
                            self.stats[item_stat_name] -= item_stat
            else:
                result = f"{item_proposed.name} is not equipped, did you mean to equip it?"
        else:
            result = "That item is None, you cannot unequip it, did you forget to pass an actual item to the unequip method?"

        return result
    
    def attack(self, target: Entity) -> str:
        """This entity attacks target entity, calculating expected damage and returning the results of the attack as a human-readable string."""
        # String to be returned summarizing the attack.
        base_result: str = ""
        additional_result: str = ""

        # calculate proposed damage and clamp to 0 if needed
        proposed_damage: int = self.stats["attack"] - target.stats["defence"]
        if proposed_damage < 0:
            proposed_damage = 0
        
        # Actually deal proposed damage!
        target.stats["health"] -= proposed_damage

        # Also report if target entity is defeated!
        if target.stats["health"] <= 0:
            target.stats["health"] = 0
            additional_result = f"\twhich defeats the {target.name} and awards {target.stats['experience']} experience to {self.name}!\n"
            # award experience, ...
            self.stats["experience"] += target.stats["experience"]
            # "drop" items into player inventory (later drop things on the ground of the target's location)
            # Note!: remember to not modify you list while you are walking through it!
            #   Build a list of item references in one phase, and then remove from the target list and add to the self list in a second phase
            items_to_be_removed: list[item.Item] = []
            for item in target.inventory:
                additional_result += self.add_item(item)
                items_to_be_removed.append(item)
            for item in items_to_be_removed:
                if item.is_equipped:
                    target.unequip(item)
                # debug
                # print(f"\ttarget.remove_item({item}): {target.remove_item(item)}\n")
        
        # Start generating result string based on proposed damage.
        base_result = f"{self.name} deals {proposed_damage} damage to {target.name}, leaving {target.stats['health']} in remaining health for {target.name}.\n"


        return base_result + additional_result

    def fight(self, target:Entity) -> str:
        """Perform one round of combat between self and target."""
        result: str = ""
        result += f"{self.name} attacks {target.name}: {self.attack(target)}\n"
        result += f"{target.name} attacks {self.name}: {target.attack(self)}\n"
        return result
