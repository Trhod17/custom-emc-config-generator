from core.items.itembase import ItemBase
from core.logger import log
from core.recipe import Recipe


class ItemEE2(ItemBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.meta = 0
        self.custom_emc_extras = False
        self.num_dusts = None
        self.dust_tier = None
        self.add_as_fuel = False
        self.unrepairable = False
        self.add_ore = False

    def parse(self, name, data, mod) -> None:
        super().parse(name, data, mod)
        self.id = data["id"]
        if "meta" in data:
            self.meta = data["meta"]
        self.emc = 0

        if "custom_emc_extras" in data:
            self.custom_emc_extras = True

            sub_data = data["custom_emc_extras"]
            print(sub_data)

            if "num_dusts" in sub_data and "dust_tier" in sub_data:
                self.num_dusts = sub_data["num_dusts"]
                self.dust_tier = sub_data["dust_tier"]

            if "add_as_fuel" in sub_data:
                self.add_as_fuel = sub_data["add_as_fuel"]

            if "unrepairable" in sub_data:
                self.unrepairable = sub_data["unrepairable"]

            if "add_ore" in sub_data:
                self.add_ore = sub_data["add_ore"]

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
