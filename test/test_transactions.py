import pytest
from test.globals import *

from src.transactions import Split, Transaction, TransactionHistory, DuplicateError, SALE, PURCHASE

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