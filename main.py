from core.app import App


def main():

    app = App()
    app.load_modpacks()
    app.create_modpack_registries()
    app.register_mods()
    app.process_recipes()
    app.process_emc()
    app.run_generators()


if __name__ == "__main__":
    main()
