

from core.items.itembase import ItemBase
from core.logger import log
from core.recipe import Recipe


class ItemPreFlattening(ItemBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.meta = 0

    def parse(self, name, data, mod) -> None:
        self.parse(name, data, mod)

        if "id" in data:
            self.id = data["id"]
        if "meta" in data:
            self.meta = data["meta"]
#         self.name = name
#         if "meta" in data:
#             self.meta = data["meta"]
#         self.emc = 0
#
#         self.mod = mod.modid
#
#         if "emc" in data:
#             self.emc = data["emc"]
#
#         if "qty_from_craft" in data:
#             self.qty = data["qty_from_craft"]
#
#         if "recipe" in data:
#             self._raw_recipe = data["recipe"]
#             self.has_recipe = True


    def parse_recipe(self, registry) -> None:
        items = []

        for raw_item in self._raw_recipe:
            item = registry.get_item(raw_item["item"])
            items.append([item, raw_item["qty"]])

        self.recipe = Recipe().parse(items)

    def parse_emc(self) -> int:
        new_emc = 0

        if not self.has_recipe:
            log.debug(f"EMC for {self.name} unchanged from {self.emc}")
            return self.emc

        for ingredient in self.recipe.items:
            if not ingredient.item.has_recipe:
                new_emc += ingredient.item.emc * ingredient.qty

            if ingredient.item.emc == 0:
                new_emc += ingredient.item.parse_emc() * ingredient.qty
                continue

            if ingredient.item.emc >= 1:
                new_emc += ingredient.item.emc * ingredient.qty

        self.emc += new_emc // self.qty
        log.debug(f"{new_emc} {self.qty}, {new_emc // self.qty}")
        log.debug(f"Setting EMC for {self.name} to {self.emc}")
        return self.emc
