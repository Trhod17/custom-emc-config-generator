from pathlib import Path

import yaml

from core.constants import config_pack_dir
from core.logger import log


class ConfigPack:
    def __init__(self):
        self.name = None
        self.cpid = None
        self.modpack_version = None
        self.config_dir = None
        self.mods = {}
        self.printers: list

    def parse(self, data, config_dirs):
        self.name = data["name"]
        self.cpid = data["cpid"]
        self.modpack_version = data["modpack_version"]
        self.config_dir = config_dirs
        self.printers = data["printers"]

        raw_mods = data["mods"]
        for raw_mod in raw_mods:
            mod = Mod()
            log.debug(f"{raw_mod}")
            mod.parse(raw_mod, raw_mods[raw_mod], self.cpid)
            self.mods.update({raw_mod: mod})

        return self


class Mod:
    def __init__(self):
        self.name = None
        self.version = None
        self.items = []

    def parse(self, name, data, cpid):
        self.name = name
        self.version = data["version"]

        for file in data["configs"]:
            fileDir = Path(f"{config_pack_dir}/{cpid}/{file}.yml")
            if fileDir.exists():
                with open(fileDir) as stream:
                    objs = yaml.safe_load(stream)
                # print(objs)
                self.items.append(objs)
                continue
            log.warn(f"Mod file missing {file}")
