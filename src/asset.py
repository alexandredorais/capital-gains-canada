from datetime import date, time
from typing import Type

from .transactions import Transaction, TransactionHistory
from .stats import Statistics

class Asset:
    
    def __init__(self, name: str) -> None:
        self._name = name
        self._tx_history = TransactionHistory()
        self._statistics = Statistics()
        self._statistics_up_to_date = True

    def get_name(self) -> str:
        return self._name
    
    def set_name(self, name: str) -> str:
        self._name = name
    
    def purchase(self, date: date, quantity: float, unit_price: float, closing_costs: float, tx_currency: str, exch_rate: float, target_currency: str, time: time = time.min) -> None:
        raise NotImplementedError
    
    def sell(self, date: date, quantity: float, unit_price: float, closing_costs: float, tx_currency: str, exch_rate: float, target_currency: str, time: time = time.min) -> None:
        raise NotImplementedError
    
    def statistics(self) -> Statistics:
        if self._statistics_up_to_date == False:

            self._statistics.recalculate_statistics(
                self._tx_history.get_data_for_statistics()
            )
            self._statistics_up_to_date = True

        return self._statistics

class AssetFactory:  # Ensure Assets are singletons (per asset name & type)
    _assets: dict[str: Asset] = {}

    @classmethod
    def get_instance(cls, name: str):
        # Force subclasses to implement this method
        raise NotImplementedError

    @classmethod
    def _get_instance(cls, name: str, asset_cls: Type[Asset]) -> Asset:
        asset = cls._assets.get(name, None)

        if asset is None:
            asset = asset_cls(name)  # new Asset
            cls._assets[name] = asset
        
        return asset
    
    @classmethod
    def list_assets(cls) -> list[str]:
        return list(cls._assets.keys())

    
class Stock(Asset):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def split(self, date: date, ratio: float) -> None:
        raise NotImplementedError

class StockFactory(AssetFactory):
    _assets: dict[str: Asset] = {}

    @classmethod
    def get_instance(cls, name: str) -> Stock:
        return cls._get_instance(name, Stock)


class RealEstate(Asset):

    def __init__(self, name: str) -> None:
        super().__init__(name)

class RealEstateFactory(AssetFactory):
    _assets: dict[str: Asset] = {}

    @classmethod
    def get_instance(cls, name:str) -> RealEstate:
        return cls._get_instance(name, RealEstate)