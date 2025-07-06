from test.globals import *

from src.transactions import Split, Transaction, TransactionHistory, DuplicateError, SALE, PURCHASE

if __name__ == '__main__':
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