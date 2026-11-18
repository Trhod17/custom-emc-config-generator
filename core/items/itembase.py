from core.constants import Era
from core.recipe import Recipe


class ItemBase:
    def __init__(self) -> None:

        self.name = None
        self._raw_recipe = []
        self.recipe: Recipe
        self.emc: int
        self.qty = 1
        self.has_recipe = False
        self.mod = None

    def parse(self, name, data, mod) -> None:
        self.name = name
        self.id = data["id"]
        if "meta" in data:
            self.meta = data["meta"]
        self.emc = 0

        self.mod = mod.name

        if "emc" in data:
            self.emc = data["emc"]

        if "qty_from_craft" in data:
            self.qty = data["qty_from_craft"]

        if "recipe" in data:
            self._raw_recipe = data["recipe"]
            self.has_recipe = True
