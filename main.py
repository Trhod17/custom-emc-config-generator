# config_packs = {}
# registries = {}

# def read_yaml_file(filename):
#     with open(f"{filename}", "r") as f:
#         output = yaml.safe_load(f)
#     return output
#
#
# def load_config_packs(configs):
#     for config_dirs in configs.iterdir():
#         for file in config_dirs.iterdir():
#             if file.is_file() and file.name == "config.yml":
#                 data = read_yaml_file(file)
#                 config_packs.update(
#                     {data["cpid"]: ConfigPack().parse(data, config_dirs)}
#                 )
#
#
# def create_config_pack_registries(configs):
#     for config in configs.values():
#         registries[config.cpid] = Registry()
#
#
# def register_items(registry, mod):
#     for item_list in mod.items:
#         for name in item_list:
#             log.debug(f"Registered Item {name} from {mod.name}")
#             item = Item()
#             item.parse(name, item_list[name], mod.name)
#             registry.add_item(name, item)
#
#
# def process_recipes(registry):
#     for item in registry.get_all_items().values():
#         log.debug(f"Parsing Recipes for {item.name}")
#         item.parse_recipe(registry)
#
#
# def run_printer(printer, pack, name, filename):
#     if name in pack.printers:
#         log.info(f"Printing {name.capitalize()} {filename} for {pack.cpid}")
#         print = printer().setup(pack)
#         print.create_file(registries[pack.cpid])


from core.app import App


def main():

    app = App()
    app.load_config_packs()
    app.create_config_pack_registries()
    app.register_mods()
    app.process_recipes()
    app.process_emc()
    app.run_printers()


# def main():
#
#     load_config_packs(config_pack_dir)
#
#     create_config_pack_registries(config_packs)
#
#     for pack in config_packs.values():
#         log.info(f"Registering Mods for {pack.cpid}")
#         for mod in pack.mods:
#             register_items(registries[pack.cpid], pack.mods[mod])
#
#         log.info(f"Processing Recipe for {pack.cpid}")
#         process_recipes(registries[pack.cpid])
#
#         log.info(f"Calculating EMC for {pack.cpid}")
#         for item in registries[pack.cpid].get_all_items().values():
#             item.parse_emc()
#
#         run_printer(CustomEmc, pack, "customemc", "CustomEMC.cfg")
#         run_printer(TekkitRestrict, pack, "tekkitrestrict", "ModModifications.yml")
#         run_printer(EssentialsWorth, pack, "essentials", "worth.yml")
#         run_printer(EssentialsItems, pack, "essentials", "items.csv")

#     log.info("Finished")


if __name__ == "__main__":
    main()
