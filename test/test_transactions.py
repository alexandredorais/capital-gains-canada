import pandas as pd
import pytest
import datetime
from test.globals import *

from src.transactions import Split, Transaction, TransactionHistory, TransactionFinder, DuplicateError, SALE, PURCHASE, SPLIT

class TestTransaction:

    def test_num_of_transactions(self):
        tx_history = TransactionHistory()
        tx1 = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx2 = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx3 = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        spl = Split(
            date= DATE,
            ratio= RATIO
        )
        tx_history.add_purchase(tx1)
        tx_history.add_purchase(tx2)
        tx_history.add_sale(tx3)
        tx_history.add_split(spl)

        assert len(tx_history) == 4
    
    @pytest.mark.skip
    #skipped, because we might not always create the TransactionHistory in chronological order...
    #e.g. tx_history.add_sale(.. Oct 2), then later tx_history.add_purchase(.. Oct 1)
    def test_no_uncovered_sale(self):
        tx_history = TransactionHistory()
        transaction = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        
        with pytest.raises(ValueError):
            tx_history.add_sale(transaction)

    def test_no_sale_as_purchase(self):
        tx_history = TransactionHistory()
        sale = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )

        with pytest.raises(ValueError):
            tx_history.add_purchase(sale)
    
    def test_no_purchase_as_sale(self):
        tx_history = TransactionHistory()
        purchase = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )

        with pytest.raises(ValueError):
            tx_history.add_sale(purchase)

    def test_add_remove_purchase(self):
        tx_history = TransactionHistory()
        purchase = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_purchase(purchase)
        tx_history.remove_purchase(purchase)

        assert len(tx_history) == 0

    def test_add_remove_purchase_copy(self):
        tx_history = TransactionHistory()
        purchase = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        purchase_copy = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_purchase(purchase)
        tx_history.remove_purchase(purchase_copy)

        assert len(tx_history) == 0


    def test_add_remove_sale(self):
        tx_history = TransactionHistory()
        sale = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_sale(sale)
        tx_history.remove_sale(sale)

        assert len(tx_history) == 0
    
    def test_add_remove_split(self):
        tx_history = TransactionHistory()
        spl = Split(
            date= DATE,
            ratio= RATIO
        )
        tx_history.add_split(spl)
        tx_history.remove_split(spl)

        assert len(tx_history) == 0

    def test_no_duplicate_purchase(self):
        tx_history = TransactionHistory()
        purchase = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_purchase(purchase)
        
        with pytest.raises(DuplicateError):
            tx_history.add_purchase(purchase)
    
    def test_no_duplicate_sale(self):
        tx_history = TransactionHistory()
        sale = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_sale(sale)
        
        with pytest.raises(DuplicateError):
            tx_history.add_sale(sale)
    
    def test_no_duplicate_split(self):
        tx_history = TransactionHistory()
        spl = Split(
            date= DATE,
            ratio= RATIO
        )
        tx_history.add_split(spl)

        with pytest.raises(DuplicateError):
            tx_history.add_split(spl)

    def test_fail_remove_inexistent_purchase(self):
        tx_history = TransactionHistory()
        purchase1 = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        purchase2 = Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_purchase(purchase1)

        with pytest.raises(KeyError):
            tx_history.remove_purchase(purchase2)
    
    def test_fail_remove_inexistent_sale(self):
        tx_history = TransactionHistory()
        sale1 = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        sale2 = Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        )
        tx_history.add_sale(sale1)

        with pytest.raises(KeyError):
            tx_history.remove_sale(sale2)
    
    def test_fail_remove_inexistent_split(self):
        tx_history = TransactionHistory()
        spl1 = Split(
            date= DATE,
            ratio= RATIO
        )
        spl2 = Split(
            date= DATE,
            ratio= RATIO + 1
        )
        tx_history.add_split(spl1)

        with pytest.raises(KeyError):
            tx_history.remove_split(spl2)
    
    def test_get_data_for_statistics(self, long_transaction_history):
        stats_input = long_transaction_history.get_data_for_statistics()
        
        # stats_input.events: dict[str, pd.DataFrame]
        df_purchases = stats_input.get(PURCHASE)
        assert type(df_purchases) == pd.DataFrame
        assert len(df_purchases) == 4
        assert (df_purchases.sort_values(['date', 'time']).head(1) == pd.DataFrame([{
            "type": PURCHASE,
            "date": DATE,
            "quantity": QUANTITY,
            "unit_price": UNIT_PRICE,
            "closing_costs": CLOSING_COSTS,
            "tx_currency": TX_CURRENCY,
            "exch_rate": EXCH_RATE,
            "target_currency": TARGET_CURRENCY,
            "time": time.min,
        }])).all().all()
        
        df_sales = stats_input.get(SALE)
        assert type(df_sales) == pd.DataFrame
        assert len(df_sales) == 4
        assert (df_sales.sort_values(['date', 'time']).head(1) == pd.DataFrame([{
            "type": SALE,
            "date": DATE,
            "quantity": QUANTITY,
            "unit_price": UNIT_PRICE,
            "closing_costs": CLOSING_COSTS,
            "tx_currency": TX_CURRENCY,
            "exch_rate": EXCH_RATE,
            "target_currency": TARGET_CURRENCY,
            "time": time.min,
        }])).all().all()
        
        df_splits = stats_input.get(SPLIT)
        assert type(df_splits) == pd.DataFrame
        assert len(df_splits) == 5
        assert (df_splits.sort_values(['date', 'time', 'ratio']).head(1) == pd.DataFrame([{
            "type": SPLIT,
            "date": DATE,
            "ratio": RATIO,
            "time": time.min,
        }])).all().all()
    
    def test_get_data_for_statistics_empty(self):
        tx_history = TransactionHistory()
        stats_input = tx_history.get_data_for_statistics()

        # empty dataframes
        assert (stats_input.get(PURCHASE) == pd.DataFrame(columns=["type", "date", "quantity", "unit_price", "closing_costs", "tx_currency", "exch_rate", "target_currency", "time"])).all().all()
        assert (stats_input.get(SALE) == pd.DataFrame(columns=["type", "date", "quantity", "unit_price", "closing_costs", "tx_currency", "exch_rate", "target_currency", "time"])).all().all()
        assert (stats_input.get(SPLIT) == pd.DataFrame(columns=["type", "date", "ratio", "time"])).all().all()


@pytest.fixture
def long_transaction_history():

    tx_history = TransactionHistory()
    purchases = [
        Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        ),
        Transaction(
            type= PURCHASE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
            time=datetime.time(hour=14, minute=12)
        ),
        Transaction(
            type= PURCHASE,
            date= DATE + datetime.timedelta(days=1),
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE + 1,
            closing_costs= CLOSING_COSTS + 1,
            tx_currency= "USD",
            exch_rate= 1,
            target_currency= "USD",
        ),
        Transaction(
            type= PURCHASE,
            date= DATE + datetime.timedelta(days=366),
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE + 1,
            closing_costs= CLOSING_COSTS + 1,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        ),
    ]

    sales = [
        Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        ),
        Transaction(
            type= SALE,
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
            time=datetime.time(hour=14, minute=12)
        ),
        Transaction(
            type= SALE,
            date= DATE + datetime.timedelta(days=1),
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE + 1,
            closing_costs= CLOSING_COSTS + 1,
            tx_currency= "USD",
            exch_rate= 1,
            target_currency= "USD",
        ),
        Transaction(
            type= SALE,
            date= DATE + datetime.timedelta(days=366),
            quantity= QUANTITY + 1,
            unit_price= UNIT_PRICE + 1,
            closing_costs= CLOSING_COSTS + 1,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY,
        ),
    ]

    splits = [
        Split(
            date= DATE,
            ratio= RATIO,
        ),
        Split(
            date= DATE,
            ratio= RATIO,
            time=datetime.time(hour=14, minute=12)
        ),
        Split(
            date= DATE + datetime.timedelta(days=1),
            ratio= RATIO,
        ),
        Split(
            date= DATE + datetime.timedelta(days=366),
            ratio= RATIO,
        ),
        Split(
            date= DATE,
            ratio= RATIO + 1,
        ),
    ]

    for purchase in purchases:
        tx_history.add_purchase(purchase)
    for sale in sales:
        tx_history.add_sale(sale)
    for split in splits:
        tx_history.add_split(split)

    return tx_history    


class TestTransactionFinderPurchase:

    @classmethod
    def setup_class(cls):
        cls.TX_TYPE = PURCHASE

    @pytest.fixture
    def tx_finder(self, long_transaction_history) -> TransactionFinder:
        return TransactionFinder(
            tx_history=long_transaction_history,
            tx_type=self.TX_TYPE
        )
    
    def test_find_all(self, tx_finder):
        list_found = tx_finder.find_all()
        assert len(list_found) == 4
    
    def test_reset(self, tx_finder):
        tx_finder.with_year(2025).find_all()
        list_found = tx_finder.reset().find_all()
        assert len(list_found) == 4

    def test_find_by_year(self, tx_finder):
        list_found = tx_finder.with_year(2024).find_all()
        assert len(list_found) == 3

    def test_find_by_year_nonexistent(self, tx_finder):
        list_found = tx_finder.with_year(2026).find_all()
        assert len(list_found) == 0

    def test_find_by_date(self, tx_finder):
        list_found = tx_finder.with_date(DATE).find_all()
        assert len(list_found) == 2

    def test_find_by_date_nonexistent(self, tx_finder):
        list_found = tx_finder.with_date(DATE + datetime.timedelta(days=2)).find_all()
        assert len(list_found) == 0

    def test_find_by_time(self, tx_finder):
        list_found = tx_finder.with_time(datetime.time(hour=14, minute=12)).find_all()
        assert len(list_found) == 1

    def test_find_by_quantity(self, tx_finder):
        list_found = tx_finder.with_quantity(QUANTITY + 1).find_all()
        assert len(list_found) == 2

    def test_find_by_unit_price(self, tx_finder):
        list_found = tx_finder.with_unit_price(UNIT_PRICE + 1).find_all()
        assert len(list_found) == 2

    def test_find_by_closing_costs(self, tx_finder):
        list_found = tx_finder.with_closing_costs(CLOSING_COSTS + 1).find_all()
        assert len(list_found) == 2

    def test_find_by_tx_currency(self, tx_finder):
        list_found = tx_finder.with_tx_currency("USD").find_all()
        assert len(list_found) == 1

    def test_find_by_exch_rate(self, tx_finder):
        list_found = tx_finder.with_exch_rate(1).find_all()
        assert len(list_found) == 1

    def test_find_by_target_currency(self, tx_finder):
        list_found = tx_finder.with_target_currency("USD").find_all()
        assert len(list_found) == 1

    def test_find_by_multiple_attributes(self, tx_finder):
        list_found = tx_finder.with_quantity(QUANTITY + 1) \
            .with_unit_price(UNIT_PRICE + 1) \
            .with_tx_currency(TX_CURRENCY) \
            .find_all()
        assert len(list_found) == 1


class TestTransactionFinderSale:

    @classmethod
    def setup_class(cls):
        cls.TX_TYPE = SALE

    @pytest.fixture
    def tx_finder(self, long_transaction_history) -> TransactionFinder:
        return TransactionFinder(
            tx_history=long_transaction_history,
            tx_type=self.TX_TYPE
        )
    
    def test_find_all(self, tx_finder):
        list_found = tx_finder.find_all()
        assert len(list_found) == 4

    def test_reset(self, tx_finder):
        tx_finder.with_year(2025).find_all()
        list_found = tx_finder.reset().find_all()
        assert len(list_found) == 4

    def test_find_by_year(self, tx_finder):
        list_found = tx_finder.with_year(2024).find_all()
        assert len(list_found) == 3

    def test_find_by_year_nonexistent(self, tx_finder):
        list_found = tx_finder.with_year(2026).find_all()
        assert len(list_found) == 0

    def test_find_by_date(self, tx_finder):
        list_found = tx_finder.with_date(DATE).find_all()
        assert len(list_found) == 2

    def test_find_by_date_nonexistent(self, tx_finder):
        list_found = tx_finder.with_date(DATE + datetime.timedelta(days=2)).find_all()
        assert len(list_found) == 0

    def test_find_by_time(self, tx_finder):
        list_found = tx_finder.with_time(datetime.time(hour=14, minute=12)).find_all()
        assert len(list_found) == 1

    def test_find_by_quantity(self, tx_finder):
        list_found = tx_finder.with_quantity(QUANTITY + 1).find_all()
        assert len(list_found) == 2

    def test_find_by_unit_price(self, tx_finder):
        list_found = tx_finder.with_unit_price(UNIT_PRICE + 1).find_all()
        assert len(list_found) == 2

    def test_find_by_closing_costs(self, tx_finder):
        list_found = tx_finder.with_closing_costs(CLOSING_COSTS + 1).find_all()
        assert len(list_found) == 2

    def test_find_by_tx_currency(self, tx_finder):
        list_found = tx_finder.with_tx_currency("USD").find_all()
        assert len(list_found) == 1

    def test_find_by_exch_rate(self, tx_finder):
        list_found = tx_finder.with_exch_rate(1).find_all()
        assert len(list_found) == 1

    def test_find_by_target_currency(self, tx_finder):
        list_found = tx_finder.with_target_currency("USD").find_all()
        assert len(list_found) == 1

    def test_find_by_multiple_attributes(self, tx_finder):
        list_found = tx_finder.with_quantity(QUANTITY + 1) \
            .with_unit_price(UNIT_PRICE + 1) \
            .with_tx_currency(TX_CURRENCY) \
            .find_all()
        assert len(list_found) == 1


class TestTransactionFinderSplit:
    
    @classmethod
    def setup_class(cls):
        cls.TX_TYPE = SPLIT

    @pytest.fixture
    def tx_finder(self, long_transaction_history) -> TransactionFinder:
        return TransactionFinder(
            tx_history=long_transaction_history,
            tx_type=self.TX_TYPE
        )
    
    def test_find_all(self, tx_finder):
        list_found = tx_finder.find_all()
        assert len(list_found) == 5

    def test_reset(self, tx_finder):
        tx_finder.with_year(2025).find_all()
        list_found = tx_finder.reset().find_all()
        assert len(list_found) == 5
    
    def test_find_by_year(self, tx_finder):
        list_found = tx_finder.with_year(2024).find_all()
        assert len(list_found) == 4

    def test_find_by_year_nonexistent(self, tx_finder):
        list_found = tx_finder.with_year(2026).find_all()
        assert len(list_found) == 0

    def test_find_by_date(self, tx_finder):
        list_found = tx_finder.with_date(DATE).find_all()
        assert len(list_found) == 3

    def test_find_by_date_nonexistent(self, tx_finder):
        list_found = tx_finder.with_date(DATE + datetime.timedelta(days=2)).find_all()
        assert len(list_found) == 0

    def test_find_by_time(self, tx_finder):
        list_found = tx_finder.with_time(datetime.time(hour=14, minute=12)).find_all()
        assert len(list_found) == 1
    
    def test_find_by_ratio(self, tx_finder):
        list_found = tx_finder.with_ratio(RATIO).find_all()
        assert len(list_found) == 4

    def test_find_by_multiple_attributes(self, tx_finder):
        list_found = tx_finder.with_date(DATE) \
            .with_ratio(RATIO + 1) \
            .find_all()
        assert len(list_found) == 1