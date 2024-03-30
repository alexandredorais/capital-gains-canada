from datetime import date, time
from dataclasses import dataclass, field
from typing import Optional

from .stats import StatsInputs

@dataclass
class Transaction:
    type: str
    date: date
    time: time
    quantity: float
    unit_price: float
    closing_costs: float
    tx_currency: str
    exch_rate: float  # value in target_currency = exch_rate * value in tx_currency
    target_currency: str

    def __post_init__(self):
        assert type in ['Sale', 'Purchase']

class TransactionHistory:

    def __init__(self) -> None:
        pass

    def add_purchase(self, purchase: Transaction) -> None:
        raise NotImplementedError
    
    def remove_purchase(self, purchase: Transaction):
        raise NotImplementedError
    
    def add_sale(self, sale: Transaction) -> None:
        raise NotImplementedError
    
    def remove_sale(self, sale: Transaction) -> None:
        raise NotImplementedError
    
    def add_split(self, date: date, ratio: float) -> None:
        raise NotImplementedError
    
    def remove_split(self, date: date, ratio: float = None) -> None:
        raise NotImplementedError
    
    def get_data_for_statistics(self) -> StatsInputs:
        raise NotImplementedError