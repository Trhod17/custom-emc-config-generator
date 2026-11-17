from core.logger import log


class Item:
    def __init__(self):
        self.name = None
        self.id = None
        self.meta = 0
        self._raw_recipe = []
        self.recipe: Recipe
        self.emc: int
        self.qty = 1
        self.has_recipe = False
        self.mod = None
        self.custom_emc_extras = False
        self.num_dusts = None
        self.dust_tier = None
        self.add_as_fuel = False
        self.unrepairable = False
        self.add_ore = False

    def parse(self, name, data, mod_name):
        self.name = name
        self.id = data["id"]
        if "meta" in data:
            self.meta = data["meta"]
        self.emc = 0
        self.mod = mod_name

        if "emc" in data:
            self.emc = data["emc"]

        if "qty_from_craft" in data:
            self.qty = data["qty_from_craft"]

        if "recipe" in data:
            self._raw_recipe = data["recipe"]
            self.has_recipe = True

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

    def parse_recipe(self, registry):
        items = []

        for raw_item in self._raw_recipe:
            item = registry.get_item(raw_item["item"])
            items.append([item, raw_item["qty"]])

        self.recipe = Recipe().parse(items)

    def parse_emc(self):
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


class Recipe:
    def __init__(self):
        self.items = []

    def parse(self, data):

        for item in data:
            self.items.append(RecipeItem().parse(item[0], item[1]))

        return self


class RecipeItem:
    def __init__(self):
        self.item = None
        self.qty = None
        self.has_recipe = True

    def parse(self, item, qty):
        self.item = item
        self.qty = qty

        return self
