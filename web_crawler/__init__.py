from web_crawler.yahoo.yahoo import Yahoo
from web_crawler.stock_base_data_model import StockBaseDataModel


# class StockBaseDataModel:
#     def __init__(self, status_code, stock_date, stock_id, trade_volume, closing_price, opening_price, highest_price,
#                  lowest_price):
#         self._stock_date = stock_date
#         self._stock_id = stock_id
#         self._trade_volume = trade_volume
#         self._closing_price = closing_price
#         self._opening_price = opening_price
#         self._highest_price = highest_price
#         self._lowest_price = lowest_price
#         self._status_code = status_code
#
#     @property
#     def stock_date(self):
#         return self._stock_date
#
#     @property
#     def trade_volume(self):
#         return self._trade_volume
#
#     @property
#     def close_price(self):
#         return self._close_price
#
#     @property
#     def open_price(self):
#         return self._open_price
#
#     @property
#     def highest_price(self):
#         return self._highest_price
#
#     @property
#     def lowest_price(self):
#         return self._lowest_price
#
#     @property
#     def status_code(self):
#         return self._status_code
