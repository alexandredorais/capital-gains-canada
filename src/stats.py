from datetime import date
from dataclasses import dataclass
import pandas as pd

@dataclass
class StatsInputs:
    events: dict[str: pd.DataFrame]

class Statistics:

    def __init__(self) -> None:
        self._history = None
        self._ACB = None  # adjusted cost base
        self._capital_gains = None
    
    def recalculate_statistics(self, inputs: StatsInputs) -> None:
        raise NotImplementedError
    
    def history_for(self, year: date.year) -> pd.DataFrame:
        raise NotImplementedError
    
    def full_history(self) -> pd.DataFrame:
        raise NotImplementedError
    
    def list_capital_gains_for(self, year: date.year) -> pd.DataFrame:
        raise NotImplementedError
    
    def total_capital_gains_for(self, year: date.year) -> float:
        raise NotImplementedError
    
    def ACB_at_end_of_day(self, date: date) -> float:
        raise NotImplementedError