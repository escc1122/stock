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
from sqlalchemy.dialects.postgresql import insert

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
    #
    # today_str = "20210618"

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

                    # https://docs.sqlalchemy.org/en/14/dialects/postgresql.html?highlight=conflict#insert-on-conflict-upsert
                    # https://stackoverflow.com/questions/7165998/how-to-do-an-upsert-with-sqlalchemy/7166559
                    insert_stmt = insert(StockBaseData).values(stock_date=today_str,
                                                               stock_id=id,
                                                               trade_volume=trade_volume,
                                                               close_price=latest_trade_price,
                                                               open_price=open_price
                                                               )

                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=['stock_date', 'stock_id'],
                        set_=dict(stock_date=today_str,
                                  stock_id=id,
                                  trade_volume=trade_volume,
                                  close_price=latest_trade_price,
                                  open_price=open_price
                                  ))

                    session.execute(do_update_stmt)
                    session.commit()

                    # stock_base_data = StockBaseData(stock_date=today_str,
                    #                                 stock_id=id,
                    #                                 trade_volume=trade_volume,
                    #                                 close_price=latest_trade_price,
                    #                                 open_price=open_price
                    #                                 )
                    #
                    # session.add(stock_base_data)
                    #
                    # session.commit()

                else:
                    print("id no found " + id)
                    no_found_id.append(id)

                    insert_stmt = insert(StockBaseData).values(stock_date=today_str,
                                                               stock_id=id,
                                                               trade_volume=-1,
                                                               close_price=-1,
                                                               open_price=-1
                                                               )

                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=['stock_date', 'stock_id'],
                        set_=dict(stock_date=today_str,
                                  stock_id=id,
                                  trade_volume=-1,
                                  close_price=-1,
                                  open_price=-1
                                  ))

                    session.execute(do_update_stmt)
                    session.commit()
                    # stock_base_data = StockBaseData(stock_date=today_str,
                    #                                 stock_id=id,
                    #                                 trade_volume=-1,
                    #                                 close_price=-1,
                    #                                 open_price=-1
                    #                                 )
                    #
                    # session.add(stock_base_data)
                    #
                    # session.commit()
    else:
        print("re")
        time.sleep(20)
        insert_table(ids)


if __name__ == '__main__':
    for ids in newarr:
        insert_table(ids)
        time.sleep(20)