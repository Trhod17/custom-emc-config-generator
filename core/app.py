import yaml

from core.configpack import ConfigPack
from core.constants import CONFIG_PACK_DIR, Era
from core.generators.customemc import CustomEmc
from core.generators.essentials import EssentialsItems, EssentialsWorth
from core.generators.generator import Generator
from core.generators.projecte import Projecte, Projecte_Old
from core.generators.tekkitrestrict import TekkitRestrict
from core.items.itemee2 import ItemEE2
from core.items.itemmodern import ItemModern
from core.items.itempreflattening import ItemPreFlattening
from core.logger import log
from core.registry import Registry


class App:
    _config_packs: dict
    _registries: dict

    def __init__(self):
        self._config_packs = {}
        self._registries = {}

    @staticmethod
    def read_yaml_file(filename):
        with open(f"{filename}", "r") as f:
            output = yaml.safe_load(f)
        return output

    def load_config_packs(self):
        for config_dirs in CONFIG_PACK_DIR.iterdir():
            for file in config_dirs.iterdir():
                if file.is_file() and file.name == "config.yml":
                    data = self.read_yaml_file(file)
                    if data["cpid"] == 'tekkitclassic':
                       continue
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
                self._register_items(self._registries[pack.cpid], pack.mods[mod], pack)

    @staticmethod
    def _create_item(item_type, name, item_list, mod):
        item = item_type()
        item.parse(name, item_list[name], mod)
        #log.debug(item)
        return item

    def _register_items(self, registry, mod, pack):
        for item_list in mod.items:
            for name in item_list:
                item = None
                # log.debug(pack.era)
                if pack.era == Era.EE2.value:
                    item = self._create_item(ItemEE2, name, item_list, mod)
                if pack.era == Era.PROJECTE_OLD.value:
                    item = self._create_item(ItemPreFlattening, name, item_list, mod)
                if pack.era == Era.PROJECTE.value:
                    item = self._create_item(ItemModern, name, item_list, mod)
                registry.add_item(name, item)
                log.debug(f"Registered Item {name} from {mod.name}")

    def process_recipes(self):
        registry: Registry
        for pack in self._config_packs.values():
            registry = self._registries[pack.cpid]
            log.info(f"Processing Recipes for {pack.cpid}")
            log.debug(registry.get_all_items())
            for item in registry.get_all_items().values():
                log.debug(
                    f"Parsing Recipe for {item.name} from {item.mod} in {pack.name}"
                )
                item.parse_recipe(registry)

    def process_emc(self):
        for pack in self._config_packs.values():
            log.info(f"Calculating EMC for {pack.cpid}")
            for item in self._registries[pack.cpid].get_all_items().values():
                item.parse_emc()

    def run_generators(self):
        for pack in self._config_packs.values():
            #print(f'{pack.name} - {pack.generators}')
            self.run_generator(CustomEmc(), "customemc", "CustomEMC.cfg", pack)
            self.run_generator(
                TekkitRestrict(), "tekkitrestrict", "ModModifications.yml", pack
                )
            self.run_generator(EssentialsWorth(), "essentials", "worth.yml", pack)
            self.run_generator(EssentialsItems(), "essentials", "items.csv", pack)

            self.run_generator(Projecte_Old(), "projecte_old", "custom_emc.cfg", pack)
            self.run_generator(Projecte(), "projecte", "custom_emc.json", pack)

    def run_generator(self, generator: Generator, name: str, filename: str, pack):
        #print(f'{name} - {pack.generators} - {pack.name}')
        if name in pack.generators:
            log.info(f"Printing {name.capitalize()} {filename} for {pack.cpid}")
            generate = generator.setup(pack)
            generate.create_file(self._registries[pack.cpid])
