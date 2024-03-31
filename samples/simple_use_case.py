from datetime import date, time

from ..src.asset import Stock, AssetFactory

if __name__ == '__main__':
    
    # initialize stock
    stock = AssetFactory.get_instance('SAP SE Stock', Stock)

    # make purchases and sales
    stock.purchase(
        date= date(2024, 1, 1),
        quantity= 10,
        unit_price= 120,
        closing_costs= 0,
        tx_currency= 'EUR',
        exch_rate= 1.451,
        target_currency= 'CAD',
    )

    stock.purchase(
        date= date(2024, 1, 2),
        quantity= 20,
        unit_price= 140,
        closing_costs= 0,
        tx_currency= 'EUR',
        exch_rate= 1.451,
        target_currency= 'CAD',
    )

    stock.sell(
        date= date(2024, 1, 3),
        quantity= 5,
        unit_price= 160,
        closing_costs= 0,
        tx_currency= 'EUR',
        exch_rate= 1.451,
        target_currency= 'CAD',
    )

    stock.purchase(
        date= date(2024, 1, 4),
        time= time(15,30,00),
        quantity= 10,
        unit_price= 120,
        closing_costs= 0,
        tx_currency= 'EUR',
        exch_rate= 1.451,
        target_currency= 'CAD',
    )

    stock.sell(
        date= date(2024, 1, 4),
        time= time(15,30,10),
        quantity= 10,
        unit_price= 120,
        closing_costs= 0,
        tx_currency= 'EUR',
        exch_rate= 1.451,
        target_currency= 'CAD',
    )

    # calculate statistics
    stock.statistics().recalculate_statistics()

    # print results
    print("Full History:")
    print(stock.statistics().full_history())

    print("\nTotal capital gains for 2024:")
    print(stock.statistics().total_capital_gains_for(2024))

    print("\nBreakdown of capital gains for 2024:")
    print(stock.statistics().list_capital_gains_for(2024))

    print("\nAdjusted Cost Base on Jan 3 2024 (end of day)")
    print(stock.statistics().ACB_at_end_of_day(date(2024, 1, 3)))