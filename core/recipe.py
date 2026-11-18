class Recipe:
    def __init__(self) -> None:
        self.items = []

    def parse(self, data):

        for item in data:
            self.items.append(RecipeItem().parse(item[0], item[1]))

        return self


class RecipeItem:
    def __init__(self) -> None:
        self.item = None
        self.qty = None
        self.has_recipe = True

    def parse(self, item, qty):
        self.item = item
        self.qty = qty

        return self
