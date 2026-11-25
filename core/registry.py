import sys

from core.logger import log


class Registry:
    _Items: dict

    def __init__(self):
        self._Items = {}

    def add_item(self, name, item):
        if name in self._Items:
            existing_registry_object = self.get_item(name)
            error = f"""Item {name} from {item.mod}, Already Exists in Registry from mod {existing_registry_object.mod}"""
            log.error(error)
            sys.exit()
        self._Items[name] = item

    def get_item(self, item: str):
        item_obj = self._Items.get(item)
        if item_obj is None:
            log.error(f"Could not Find Item: {item}")
            sys.exit()
        return item_obj

    def get_all_items(self):
        return self._Items
