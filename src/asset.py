from datetime import date, time

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
        
    
class Stock(Asset):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def split(self, date: date, ratio: float) -> None:
        raise NotImplementedError