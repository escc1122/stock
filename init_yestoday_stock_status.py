# -*- coding: utf-8 -*-
"""
初始化昨天交易資料
"""

import twstock
import customer_db
import numpy as np
import time


stock_array = customer_db.get_stock_ids()

newarr = np.array_split(stock_array, int(len(stock_array) / 150) + 1)

# print (newarr[0].tolist())

# # print (stock_array)

error_ids = []
no_found_id = []


def insert_table(ids):
    stocks = twstock.realtime.get(ids.tolist())
    print(stocks['success'])
    if stocks['success'] == True:
        for id in ids:
            if id not in twstock.twse:
                print("test " + id)
                twstock.twse[id] = {}

        customer_db.get_connect()
        conn = customer_db.get_connect()
        cursor = conn.cursor()
        for id in ids:
            if id in stocks:
                realtime = stocks[id]['realtime']
                latest_trade_price = realtime['latest_trade_price']
                open_price = realtime['open']
                if open_price == '-':
                    open_price = '-1'
                if latest_trade_price == '-':
                    latest_trade_price = '-1'
                cursor.execute(
                    "INSERT INTO yestoday_stock_status (stock_id, trade_volume, close_price, open_price) VALUES (%s, "
                    "%s, %s, %s) on conflict (stock_id) do update set trade_volume=%s;",
                    (id, realtime['accumulate_trade_volume'], latest_trade_price, open_price,
                     realtime['accumulate_trade_volume']))
            else:
                print("id no found " + id)
                no_found_id.append(id)
                cursor.execute(
                    "INSERT INTO yestoday_stock_status (stock_id, trade_volume, close_price, open_price) VALUES (%s, "
                    "%s, %s, %s) on conflict (stock_id) do update set trade_volume=0;",
                    (id, '-1', '-1', '-1'))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        print("re")
        time.sleep(20)
        insert_table(ids)


def clean_table():
    print("cleanTable")
    customer_db.get_connect()
    conn = customer_db.get_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM public.yestoday_stock_status")
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    clean_table()
    for ids in newarr:
        insert_table(ids)
        time.sleep(20)
