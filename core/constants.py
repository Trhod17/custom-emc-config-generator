from enum import Enum
from pathlib import Path

CONFIG_PACK_DIR = Path("packs")


class Era(Enum):
    #Equivalent Exchange 2 Era 1.1(If CustomEMC mod is available) - 1.2.5
    EE2 = "ee2"
    #ProjectE 1.7.10 - 1.12.2
    PROJECTE_OLD = "projecte_old"
    #ProjectE
    PROJECTE = "projecte"
