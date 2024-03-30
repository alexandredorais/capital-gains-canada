from .asset import Asset

class DataImport:

    def __init__(self, asset: Asset, import_filepath) -> None:
        self._asset = asset
        self._import_filepath = import_filepath

    def import_data(self):
        raise NotImplementedError
    

class DataImportFromEquate(DataImport):

    def __init__(self, asset: Asset, import_filepath) -> None:
        super().__init__(asset, import_filepath)

    def import_data(self):
        raise NotImplementedError