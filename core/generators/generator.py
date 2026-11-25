class Generator:
    def __init__(self):
        self.output_file_name = None
        self.pack = None

    def setup(self, pack):
        self.pack = pack
        return self

    def create_file(self, registry):
        pass

    @staticmethod
    def get_path(modpack_id, version, path):
        output_dir = f"output/{modpack_id}/{version}/{path}/"
        return output_dir
