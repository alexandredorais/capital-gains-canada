from .asset import Asset

class FileManager:

    def __init__(self, asset: Asset, input_filepath: str = None, output_filepath: str = None) -> None:
        self._asset = asset
        self._input_filepath = input_filepath
        self._output_filepath = output_filepath

    def set_input_filepath(self, filepath: str) -> None:
        self._input_filepath = filepath
    
    def set_output_filepath(self, filepath: str) -> None:
        self._output_filepath = filepath

    def load_history(self) -> None:
        raise NotImplementedError

    def save_history(self) -> None:
        raise NotImplementedError
    

class CSVFileManager(FileManager):

    def __init__(self, asset: Asset) -> None:
        super().__init__(asset)

    def load_history(self) -> None:
        raise NotImplementedError
    
    def save_history(self) -> None:
        raise NotImplementedError