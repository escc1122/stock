import datetime
import threading

import requests
import json
from web_crawler.stock_base_data_model import StockBaseDataModel
import time


class Yahoo:
    _url = "https://tw.quote.finance.yahoo.net/quote/q"

    @classmethod
    def get_stock_data_by_stock_id(cls, stock_id) -> (int, [StockBaseDataModel]):
        with threading.RLock() as lock:
            time.sleep(3)
            return cls.__get_stock_data_by_stock_id(stock_id)

    @classmethod
    def __get_stock_data_by_stock_id(cls, stock_id) -> (int, [StockBaseDataModel]):
        print("__get_stock_data_by_stock_id start")
        stock_base_data_model_list = []
        now_time = int(datetime.datetime.now().timestamp())
        callback = 'jQuery111306841563040442273_1624119985933'
        stock_id = stock_id.upper()
        my_params = {'type': 'ta',
                     'perd': 'd',
                     'mkt': '10',
                     'sym': stock_id,
                     'v': '1',
                     'callback': callback,
                     '_': now_time
                     }
        res = requests.get(cls._url, params=my_params)
        status_code = -1
        if 200 == res.status_code:
            bbb = res.text
            bbb = bbb.replace(callback + "(", "").replace(");", "")
            status_code = res.status_code
            try:
                ccc = json.loads(bbb)
            except Exception as e:
                ccc = {'ta': []}

            ta = ccc["ta"]
            for stock_data in ta:
                stock_date = stock_data['t']
                trade_volume = stock_data['v']
                close_price = stock_data['c']
                open_price = stock_data['o']
                highest_price = stock_data['h']
                lowest_price = stock_data['l']
                stock_base_data_model = StockBaseDataModel(status_code=status_code,
                                                           stock_date=stock_date,
                                                           stock_id=stock_id,
                                                           trade_volume=trade_volume,
                                                           closing_price=close_price,
                                                           opening_price=open_price,
                                                           highest_price=highest_price,
                                                           lowest_price=lowest_price
                                                           )
                stock_base_data_model_list.append(stock_base_data_model)
        else:
            stock_base_data_model = StockBaseDataModel(status_code=status_code, stock_id=stock_id)
            stock_base_data_model_list.append(stock_base_data_model)
        return status_code, stock_base_data_model_list
