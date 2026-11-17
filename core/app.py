import yaml

from core.configpack import ConfigPack
from core.constants import config_pack_dir
from core.item import Item
from core.logger import log
from core.printer import (
    CustomEmc,
    EssentialsItems,
    EssentialsWorth,
    Printer,
    TekkitRestrict,
)
from core.registry import Registry


class App:
    _config_packs: dict
    _registries: dict

    def __init__(self):
        self._config_packs = {}
        self._registries = {}

    def read_yaml_file(self, filename):
        with open(f"{filename}", "r") as f:
            output = yaml.safe_load(f)
        return output

    def load_config_packs(self):
        for config_dirs in config_pack_dir.iterdir():
            for file in config_dirs.iterdir():
                if file.is_file() and file.name == "config.yml":
                    data = self.read_yaml_file(file)
                    self._config_packs.update(
                        {data["cpid"]: ConfigPack().parse(data, config_dirs)}
                    )

    def create_config_pack_registries(self):
        for config in self._config_packs.values():
            self._registries[config.cpid] = Registry()

    def register_mods(self):
        for pack in self._config_packs.values():
            log.info(f"Registering Mods for {pack.cpid}")
            for mod in pack.mods:
                self._register_items(self._registries[pack.cpid], pack.mods[mod])

    def _register_items(self, registry, mod):
        for item_list in mod.items:
            for name in item_list:
                log.debug(f"Registered Item {name} from {mod.name}")
                item = Item()
                item.parse(name, item_list[name], mod.name)
                registry.add_item(name, item)

    def process_recipes(self):
        registry: Registry
        for pack in self._config_packs.values():
            registry = self._registries[pack.cpid]
            log.info(f"Processing Recipes for {pack.cpid}")
            for item in registry.get_all_items().values():
                log.debug(f"Parsing Recipe for {item.name}")
                item.parse_recipe(registry)

    def process_emc(self):
        for pack in self._config_packs.values():
            log.info(f"Calculating EMC for {pack.cpid}")
            for item in self._registries[pack.cpid].get_all_items().values():
                item.parse_emc()

    def run_printers(self):
        self.run_printer(CustomEmc(), "customemc", "CustomEMC.cfg")
        self.run_printer(TekkitRestrict(), "tekkitrestrict", "ModModifications.yml")
        self.run_printer(EssentialsWorth(), "essentials", "worth.yml")
        self.run_printer(EssentialsItems(), "essentials", "items.csv")

    def run_printer(self, printer: Printer, name: str, filename: str):
        for pack in self._config_packs.values():
            if name in pack.printers:
                log.info(f"Printing {name.capitalize()} {filename} for {pack.cpid}")
                print = printer.setup(pack)
                print.create_file(self._registries[pack.cpid])
