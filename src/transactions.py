from datetime import date, time
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

from .stats import StatsInputs

SALE = 'Sale'
PURCHASE = 'Purchase'

class DuplicateError(ValueError):
    pass

@dataclass
class Transaction:
    type: str
    date: date
    quantity: float
    unit_price: float
    closing_costs: float
    tx_currency: str
    exch_rate: float  # value in target_currency = exch_rate * value in tx_currency
    target_currency: str
    time: time = time.min

    def __post_init__(self):
        assert self.type in [SALE, PURCHASE]

@dataclass
class Split:
    date: date
    ratio: float
    time: time = time.min

class TransactionHistory:

    def __init__(self) -> None:
        # {year: {date: [Transaction,]}}
        self._sales: dict[date.year: dict[date: list[Transaction]]] = {}
        self._purchases: dict[date.year: dict[date: list[Transaction]]] = {}
        self._splits: dict[date.year: dict[date: list[Split]]] = {}

    def __len__(self) -> int:
        return self._len_nested_dict(self._sales) \
                + self._len_nested_dict(self._purchases) \
                + self._len_nested_dict(self._splits)

    def add_purchase(self, purchase: Transaction) -> None:
        if purchase.type != PURCHASE:
            raise ValueError(f"Transaction is not a purchase.\n{purchase}")
        
        self._append_dict(self._purchases, purchase)
    
    def remove_purchase(self, purchase: Transaction) -> None:
        self._pop_from_dict(self._purchases, purchase)
    
    def add_sale(self, sale: Transaction) -> None:
        if sale.type != SALE:
            raise ValueError(f"Transaction is not a sale.\n{sale}")
        
        self._append_dict(self._sales, sale)
    
    def remove_sale(self, sale: Transaction) -> None:
        self._pop_from_dict(self._sales, sale)
    
    def add_split(self, split: Split) -> None:
        self._append_dict(self._splits, split)
    
    def remove_split(self, split: Split) -> None:
        self._pop_from_dict(self._splits, split)
    
    def get_data_for_statistics(self) -> StatsInputs:
        raise NotImplementedError
    
    def _append_dict(self, attr_dict: dict, new_obj: Transaction | Split) -> None:
        date = new_obj.date
        year = date.year
        
        active_year = attr_dict.get(year)
        active_date = None
        contains_duplicate = False
        if active_year is not None:
            active_date = active_year.get(date)
        if active_date is not None:
            contains_duplicate = any([True for obj in active_date if obj == new_obj])
        
        if contains_duplicate == True:
            # duplicate exists
            raise DuplicateError(f"Duplicate record.\n{new_obj}")
        elif active_date is not None:
            # date already exists
            active_date.append(new_obj)
        elif active_date is None and active_year is not None:
            # date doesn't exist yet but year already exists
            active_year.update({date: [new_obj]})
        else:
            # year and date don't exist yet
            attr_dict.update({year: {date: [new_obj]}})

    def _pop_from_dict(self, attr_dict: dict, obj_to_remove: Transaction | Split) -> None:
        date = obj_to_remove.date
        year = date.year
        key_error_text = f"Record does not exist.\n{obj_to_remove}"

        active_year = attr_dict.get(year)
        if active_year is None:
            raise KeyError(key_error_text)
        
        active_date = active_year.get(date)
        if active_date is None:
            raise KeyError(key_error_text)
        
        try:
            active_date.remove(obj_to_remove)
        except ValueError:
            raise KeyError(key_error_text)
        
    def _len_nested_dict(self, attr_dict: dict) -> int:
        total_len = 0
        for year, sub_dict in attr_dict.items():
            for date, sub_list in sub_dict.items():
                total_len += len(sub_list)
        return total_len