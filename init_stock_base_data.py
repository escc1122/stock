# -*- coding: utf-8 -*-
"""
初始化昨天交易資料
"""

import twstock
import customer_db
import numpy as np
import time
from model.stock_base_data import StockBaseData
from sqlalchemy.orm import sessionmaker
import datetime
from customer_db import SqlAlchemy

stock_array = customer_db.get_stock_ids()

newarr = np.array_split(stock_array, int(len(stock_array) / 150) + 1)

error_ids = []
no_found_id = []


def insert_table(ids):
    stocks = twstock.realtime.get(ids.tolist())
    print(stocks['success'])
    engine = SqlAlchemy.get_engine()
    Session = sessionmaker(bind=engine)
    today = datetime.datetime.today()
    today_str = "{}{:0>2d}{:0>2d}".format(today.year, today.month, today.day)

    if stocks['success']:
        for id in ids:
            if id not in twstock.twse:
                print("test " + id)
                twstock.twse[id] = {}

        with Session() as session:
            for id in ids:
                if id in stocks:
                    realtime = stocks[id]['realtime']
                    latest_trade_price = realtime['latest_trade_price']
                    open_price = realtime['open']
                    trade_volume = realtime['accumulate_trade_volume']
                    if open_price == '-':
                        open_price = '-1'
                    if latest_trade_price == '-':
                        latest_trade_price = '-1'

                    stock_base_data = StockBaseData(stock_date=today_str,
                                                    stock_id=id,
                                                    trade_volume=trade_volume,
                                                    close_price=latest_trade_price,
                                                    open_price=open_price
                                                    )

                    session.add(stock_base_data)

                    session.commit()

                else:
                    print("id no found " + id)
                    no_found_id.append(id)
                    stock_base_data = StockBaseData(stock_date=today_str,
                                                    stock_id=id,
                                                    trade_volume=-1,
                                                    close_price=-1,
                                                    open_price=-1
                                                    )

                    session.add(stock_base_data)

                    session.commit()
    else:
        print("re")
        time.sleep(20)
        insert_table(ids)


if __name__ == '__main__':
    for ids in newarr:
        insert_table(ids)
        time.sleep(20)
