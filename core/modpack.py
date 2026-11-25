import sys
from pathlib import Path

import yaml

from core.constants import MODPACKS_DIR
from core.logger import log


class ModPack:
    def __init__(self):
        self.name = None
        self.modpack_id = None
        self.modpack_version = None
        self.game_version: str
        self.era = None
        self.config_dir = None
        self.mods = {}
        self.generators: list

    @staticmethod
    def required(data, element):
        if data["name"] is None:
            log.error(f"modpack.yml Missing Required Element {element}")
            sys.exit()
        return data[element]

    @staticmethod
    def optional(data, element):
        if element in data:
            return data[element]
        return None

    def parse(self, data):
        self.name = self.required(data, "name")
        self.modpack_id = self.required(data, "modpack_id")
        self.game_version = self.required(data, "game_version")
        self.modpack_version = self.optional(data, "modpack_version")
        self.generators = self.required(data, "generators")
        self.era = self.required(data, "era")

        raw_mods = self.required(data, "mods")
        for raw_mod in raw_mods:
            mod = Mod()
            log.debug(f"{raw_mod}")
            mod.parse(raw_mod, raw_mods[raw_mod], self.modpack_id)
            self.mods.update({raw_mod: mod})

        return self


class Mod:
    def __init__(self):
        self.name = None
        self.modid = None
        self.version = None
        self.items = []

    def parse(self, name, data, cpid):
        self.name = name
        self.version = data["version"]

        if "modid" in data:
            self.modid = data["modid"]

        for file in data["configs"]:
            fileDir = Path(f"{MODPACKS_DIR}/{cpid}/{file}.yml")
            if fileDir.exists():
                with open(fileDir) as stream:
                    objs = yaml.safe_load(stream)
                # print(objs)
                self.items.append(objs)
                continue
            log.warn(f"Mod file missing {file}")
