import yaml

from core.constants import MODPACKS_DIR, Era
from core.generators.customemc import CustomEmc
from core.generators.essentials import EssentialsItems, EssentialsWorth
from core.generators.generator import Generator
from core.generators.projecte import Projecte, ProjecteOld
from core.generators.tekkitrestrict import TekkitRestrict
from core.items.itemee2 import ItemEE2
from core.items.itemmodern import ItemModern
from core.items.itempreflattening import ItemPreFlattening
from core.logger import log
from core.modpack import ModPack
from core.registry import Registry


class App:
    _modpacks: dict
    _registries: dict

    def __init__(self):
        self._modpacks = {}
        self._registries = {}

    @staticmethod
    def read_yaml_file(filename):
        with open(f"{filename}", "r") as f:
            output = yaml.safe_load(f)
        return output

    def load_modpacks(self):

        for modpack_dir in MODPACKS_DIR.iterdir():
            for file in modpack_dir.iterdir():
                if file.is_file() and file.name == "modpack.yml":
                    data = self.read_yaml_file(file)
                    # if data["modpack_id"] == 'tekkitclassic':
                    #   continue
                    self._modpacks.update({data["modpack_id"]: ModPack().parse(data)})

    def create_modpack_registries(self):
        for modpack in self._modpacks.values():
            self._registries[modpack.modpack_id] = Registry()

    def register_mods(self):
        for pack in self._modpacks.values():
            log.info(f"Registering Mods for {pack.modpack_id}")
            for mod in pack.mods:
                self._register_items(
                    self._registries[pack.modpack_id], pack.mods[mod], pack
                )

    @staticmethod
    def _create_item(item_type, name, item_list, mod):
        item = item_type()
        item.parse(name, item_list[name], mod)
        # log.debug(item)
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
        for pack in self._modpacks.values():
            registry = self._registries[pack.modpack_id]
            log.info(f"Processing Recipes for {pack.modpack_id}")
            for item in registry.get_all_items().values():
                log.debug(
                    f"Parsing Recipe for {item.name} from {item.mod} in {pack.name}"
                )
                item.parse_recipe(registry)

    def process_emc(self):
        for pack in self._modpacks.values():
            log.info(f"Calculating EMC for {pack.modpack_id}")
            for item in self._registries[pack.modpack_id].get_all_items().values():
                item.parse_emc()

    def run_generators(self):
        for pack in self._modpacks.values():
            # print(f'{pack.name} - {pack.generators}')
            self.run_generator(CustomEmc(), "customemc", "CustomEMC.cfg", pack)
            self.run_generator(
                TekkitRestrict(), "tekkitrestrict", "ModModifications.yml", pack
            )
            self.run_generator(EssentialsWorth(), "essentials", "worth.yml", pack)
            self.run_generator(EssentialsItems(), "essentials", "items.csv", pack)

            self.run_generator(ProjecteOld(), "projecte_old", "custom_emc.cfg", pack)
            self.run_generator(Projecte(), "projecte", "custom_emc.json", pack)

    def run_generator(self, generator: Generator, name: str, filename: str, pack):
        # print(f'{name} - {pack.generators} - {pack.name}')
        if name in pack.generators:
            log.info(f"Printing {name.capitalize()} {filename} for {pack.modpack_id}")
            generate = generator.setup(pack)
            generate.create_file(self._registries[pack.modpack_id])
