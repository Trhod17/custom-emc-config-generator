from core.app import App


def main():

    app = App()
    app.load_config_packs()
    app.create_config_pack_registries()
    app.register_mods()
    app.process_recipes()
    app.process_emc()
    app.run_printers()


if __name__ == "__main__":
    main()
