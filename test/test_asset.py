import pytest
from test.globals import *

from src.asset import Asset, Stock, RealEstate, AssetFactory, StockFactory, RealEstateFactory

class TestAsset:

    def test_purchase_voids_statistics(self):
        asset = Asset(NAME)
        asset._statistics_up_to_date = True

        asset.purchase(
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY
        )

        assert asset._statistics_up_to_date == False
    
    def test_sale_voids_statistics(self):
        asset = Asset(NAME)
        asset.purchase(
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY
        )  # need a purchase to avoid selling an uncovered postion (i.e. selling an asset you don't have)

        asset._statistics_up_to_date = True
        
        asset.sell(
            date= DATE,
            quantity= QUANTITY,
            unit_price= UNIT_PRICE,
            closing_costs= CLOSING_COSTS,
            tx_currency= TX_CURRENCY,
            exch_rate= EXCH_RATE,
            target_currency= TARGET_CURRENCY
        )

        assert asset._statistics_up_to_date == False


class TestStock:

    def test_split_voids_statistics(self):
        stock = Stock(NAME)
        stock._statistics_up_to_date = True

        stock.split(
            date= DATE,
            ratio= RATIO
        )

        assert stock._statistics_up_to_date == False


class TestAssetFactory:

    def test_get_instance_not_impl(self):
        with pytest.raises(NotImplementedError):
            AssetFactory.get_instance(NAME)


class TestSubFactories:

    def test_subclasses_non_interference(self):
        COMMON_VALUE_A = 1
        COMMON_VALUE_B = 2  # != COMMON_VALUE_A

        asset1 = StockFactory.get_instance(NAME)
        asset1._statistics = COMMON_VALUE_A

        asset2 = RealEstateFactory.get_instance(NAME)
        asset2._statistics = COMMON_VALUE_B

        assert asset1._statistics != asset2._statistics

    def test_stock_singleton(self):
        COMMON_VALUE = 1

        asset1 = StockFactory.get_instance(NAME)
        asset1._statistics = COMMON_VALUE
        
        asset2 = StockFactory.get_instance(NAME)

        assert asset2._statistics == COMMON_VALUE
    
    def test_stock_non_interference(self):
        COMMON_VALUE_A = 1
        COMMON_VALUE_B = 2  # != COMMON_VALUE_A
        DIFFERENT_NAME = NAME + '_'

        asset1 = StockFactory.get_instance(NAME)
        asset1._statistics = COMMON_VALUE_A

        asset2 = StockFactory.get_instance(DIFFERENT_NAME)
        asset2._statistics = COMMON_VALUE_B

        assert asset1._statistics != asset2._statistics
    
    def test_list_stocks(self):
        DIFFERENT_NAME = NAME + '_'

        StockFactory.get_instance(NAME)
        StockFactory.get_instance(DIFFERENT_NAME)

        assert StockFactory.list_assets() == [ NAME, DIFFERENT_NAME ] \
            or StockFactory.list_assets() == [ DIFFERENT_NAME, NAME ]

    def test_real_estate_singleton(self):
        COMMON_VALUE = 1

        asset1 = RealEstateFactory.get_instance(NAME)
        asset1._statistics = COMMON_VALUE
        
        asset2 = RealEstateFactory.get_instance(NAME)

        assert asset2._statistics == COMMON_VALUE
    
    def test_real_estate_non_interference(self):
        COMMON_VALUE_A = 1
        COMMON_VALUE_B = 2  # != COMMON_VALUE_A
        DIFFERENT_NAME = NAME + '_'

        asset1 = RealEstateFactory.get_instance(NAME)
        asset1._statistics = COMMON_VALUE_A

        asset2 = RealEstateFactory.get_instance(DIFFERENT_NAME)
        asset2._statistics = COMMON_VALUE_B

        assert asset1._statistics != asset2._statistics
    
    def test_list_real_estate(self):
        DIFFERENT_NAME = NAME + '_'

        RealEstateFactory.get_instance(NAME)
        RealEstateFactory.get_instance(DIFFERENT_NAME)

        assert RealEstateFactory.list_assets() == [ NAME, DIFFERENT_NAME ] \
            or RealEstateFactory.list_assets() == [ DIFFERENT_NAME, NAME ]