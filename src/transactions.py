from __future__ import annotations
from datetime import date, time
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

from .stats import StatsInputs

SALE = 'Sale'
PURCHASE = 'Purchase'
SPLIT = 'Split'

def flatten_dict_to_list(d):
    # takes a nested dict and flattens its leaf values into a list
    items = []
    for v in d.values():
        if isinstance(v, dict):
            items.extend(flatten_dict_to_list(v))
        else:
            items.extend(v)
    return items

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

    @staticmethod
    def columns():
        return ["type", "date", "quantity", "unit_price", "closing_costs", "tx_currency", "exch_rate", "target_currency", "time"]

    def __post_init__(self):
        assert self.type in [SALE, PURCHASE]

    def to_dict(self):
        return {
            "type": self.type,
            "date": self.date,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "closing_costs": self.closing_costs,
            "tx_currency": self.tx_currency,
            "exch_rate": self.exch_rate,
            "target_currency": self.target_currency,
            "time": self.time,
        }

@dataclass
class Split:
    date: date
    ratio: float
    type: str = SPLIT
    time: time = time.min

    @staticmethod
    def columns():
        return ["type", "date", "ratio", "time"]

    def to_dict(self):
        return {
            "type": self.type,
            "date": self.date,
            "ratio": self.ratio,
            "time": self.time,
        }

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
        sales_dicts = [item.to_dict() for item in flatten_dict_to_list(self._sales)]
        purchases_dicts = [item.to_dict() for item in flatten_dict_to_list(self._purchases)]
        splits_dicts = [item.to_dict() for item in flatten_dict_to_list(self._splits)]

        return {
            SALE: pd.DataFrame(sales_dicts, columns=Transaction.columns()),
            PURCHASE: pd.DataFrame(purchases_dicts, columns=Transaction.columns()),
            SPLIT: pd.DataFrame(splits_dicts, columns=Split.columns()),
        }
    
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

class TransactionFinder: 
    # useful class e.g. if we want to delete certain transactions from the transaction history,
    # we can identify them first with TransactionFinder, 
    # and then delete them with the methods provided by TransactionHistory

    def __init__(self, tx_history: TransactionHistory, tx_type: str):
        self._tx_history = tx_history
        self._type = tx_type # SALE / PURCHASE / SPLIT
        self._year = None
        self._date = None
        self._search_parameters = {}
                                # time
                                # ratio
                                # quantity
                                # unit_price
                                # closing_costs
                                # tx_currency
                                # exch_rate
                                # target_currency
    
    def reset(self):
        return TransactionFinder(
            tx_history=self._tx_history,
            tx_type=self._type
        )

    def with_year(self, year: date.year) -> TransactionFinder:
        # year should be handled differently from other search parameters, because it's a dictionary key of TransactionHistory
        if self._date is not None:
            assert self._date.year == year, "Date and year must match"
        self._year = year
        return self

    def with_date(self, date: date) -> TransactionFinder:
        # date should be handled differently from other search parameters, because it's a (nested) dictionary key of TransactionHistory
        if self._year is not None:
            assert self._year == date.year, "Date and year must match"
        self._date = date
        return self

    def with_time(self, time: time) -> TransactionFinder:
        self._search_parameters["time"] = time
        return self

    def with_ratio(self, ratio: float) -> TransactionFinder:
        if self._type != SPLIT:
            raise NameError(f"Method 'with_ratio' should not be called in this context: transaction type = {self._type}")
        self._search_parameters["ratio"] = ratio
        return self

    def with_quantity(self, quantity: float) -> TransactionFinder:
        self._search_parameters["quantity"] = quantity
        return self

    def with_unit_price(self, unit_price: float) -> TransactionFinder:
        self._search_parameters["unit_price"] = unit_price
        return self

    def with_closing_costs(self, closing_costs: float) -> TransactionFinder:
        self._search_parameters["closing_costs"] = closing_costs
        return self

    def with_tx_currency(self, tx_currency: str) -> TransactionFinder:
        self._search_parameters["tx_currency"] =  tx_currency
        return self

    def with_exch_rate(self, exch_rate: float) -> TransactionFinder:
        self._search_parameters["exch_rate"] = exch_rate
        return self

    def with_target_currency(self, target_currency: str) -> TransactionFinder:
        self._search_parameters["target_currency"] = target_currency
        return self

    def find_all(self) -> list[Transaction | Split]:
        # Set the correct search space based on transaction type
        if self._type == SALE:
            search_space = self._tx_history._sales
        elif self._type == PURCHASE:
            search_space = self._tx_history._purchases
        elif self._type == SPLIT:
            search_space = self._tx_history._splits
        else:
            raise ValueError(f"Type '{self._type}' is not allowed.")
        
        # restrict search space by date and year (if provided)
        # if date is provided, search inside relevant list
        if self._date is not None:
            date_dict = search_space.get(self._date.year)
            if date_dict is None:
                return []
            candidates_list = date_dict.get(self._date)
            
        # if date is not provided but year is provided, flatten all date dicts from that year into one list and search inside that list
        elif self._year is not None:
            date_dict = search_space.get(self._year)
            if date_dict is None:
                return []
            candidates_list = flatten_dict_to_list(date_dict)

        # if neither date nor year is provided, flatten all dicts from all years into one list and search inside that list
        else:
            candidates_list = flatten_dict_to_list(search_space)

        # return early if we have no candidates remaining
        if candidates_list is None or candidates_list == []:
            return []
        
        # create final list of transactions found
        transctions_found = []
        for candidate in candidates_list:
            successful = True
            for parameter, expected_value in self._search_parameters.items():
                # ensure that all search criteria are respected
                successful = successful and getattr(candidate, parameter) == expected_value
            if successful:
                transctions_found.append(candidate)
        
        return transctions_found