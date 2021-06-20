# -*- coding: utf-8 -*-
"""
初始化昨天交易資料
"""

import twstock
import customer_db
import numpy as np
import time
# from model.stock_base_data import StockBaseData
from model import StockBaseData
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


def test_twse(stock_date):
    import requests
    engine = SqlAlchemy.get_engine()
    Session = sessionmaker(bind=engine)
    # {"stat":"OK","date":"20210619","title":"110年06月 2330 台積電           各日成交資訊","fields":["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"],"data":[["110/06/01","18,405,285","10,985,893,229","598.00","599.00","595.00","598.00","+1.00","20,318"],["110/06/02","22,416,789","13,362,065,937","600.00","600.00","593.00","595.00","-3.00","25,170"],["110/06/03","31,703,679","18,939,839,664","600.00","600.00","596.00","596.00","+1.00","20,749"],["110/06/04","16,072,580","9,521,252,157","591.00","595.00","590.00","595.00","-1.00","19,112"],["110/06/07","17,729,179","10,471,176,330","594.00","595.00","583.00","592.00","-3.00","25,364"],["110/06/08","14,083,552","8,312,653,665","590.00","595.00","588.00","589.00","-3.00","14,051"],["110/06/09","21,575,159","12,618,113,390","586.00","588.00","583.00","586.00","-3.00","36,405"],["110/06/10","29,741,770","17,696,413,894","591.00","599.00","587.00","599.00","+13.00","30,487"],["110/06/11","24,940,705","15,011,140,567","602.00","603.00","600.00","602.00","+3.00","25,271"],["110/06/15","30,245,897","18,415,370,774","607.00","609.00","606.00","609.00","+7.00","33,515"],["110/06/16","28,624,508","17,401,326,587","608.00","608.00","605.00","605.00","-4.00","25,816"],["110/06/17","26,477,032","15,924,656,516","601.00","606.00","598.00","606.00","X0.00","21,061"],["110/06/18","42,036,170","25,373,026,235","608.00","608.00","601.00","603.00","-3.00","16,899"]],"notes":["符號說明:+/-/X表示漲/跌/不比價","當日統計資訊含一般、零股、盤後定價、鉅額交易，不含拍賣、標購。","ETF證券代號第六碼為K、M、S、C者，表示該ETF以外幣交易。"]}
    link = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210619&stockNo=2330&_=1624090172927"
    now_time = int(datetime.datetime.now().timestamp())
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
    # my_params = {'response': 'json',
    #              'date': stock_date,
    #              'stockNo': '2330',
    #              '_': now_time
    #              }
    #
    # res = requests.get(url, params=my_params)

    # print(res.status_code == 200)
    with Session() as session:
        stock_id_list = session.execute("SELECT  distinct  stock_id FROM public.stocks;").fetchall()
        for row in stock_id_list:
            stock_id = row["stock_id"]
            my_params = {'response': 'json',
                         'date': stock_date,
                         'stockNo': stock_id,
                         '_': now_time
                         }

            res = requests.get(url, params=my_params)
            if 200 == res.status_code:
                res_data = res.json()
                if res_data["stat"] == "OK":
                    data = res_data["data"]
                    for one_data in data:
                        # ["日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]
                        stock_date = one_data[0].replace("110/", "2021").replace("/", "")
                        trade_volume = one_data[1].replace(",", "")
                        if trade_volume == "--":
                            trade_volume = -1
                        close_price = one_data[6].replace(",", "")
                        if close_price == "--":
                            close_price = -1
                        open_price = one_data[3].replace(",", "")
                        if open_price == "--":
                            open_price = -1
                        highest_price = one_data[4].replace(",", "")
                        if highest_price == "--":
                            highest_price = -1
                        lowest_price = one_data[5].replace(",", "")
                        if lowest_price == "--":
                            lowest_price = -1

                        insert_para = dict(stock_date=stock_date,
                                           stock_id=stock_id,
                                           trade_volume=trade_volume,
                                           closing_price=close_price,
                                           opening_price=open_price,
                                           highest_price=highest_price,
                                           lowest_price=lowest_price
                                           )

                        insert_stmt = insert(StockBaseData).values(insert_para)
                        do_update_stmt = insert_stmt.on_conflict_do_update(
                            index_elements=['stock_date', 'stock_id'],
                            set_=insert_para)

                        session.execute(do_update_stmt)
                        session.commit()
            else:
                print("error" + stock_id)

        print(stock_id)
        time.sleep(7)


def test():
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(
        "https://tw.stock.yahoo.com/q/q?s=" + '9941a')
    soup = BeautifulSoup(response.text.replace("加到投資組合", ""), "lxml")

    stock_date = soup.find(
        "font", {"class": "tt"}).getText().strip()[-9:]  # 資料日期

    tables = soup.find_all("table")[2]  # 取得網頁中第三個表格
    tds = tables.find_all("td")[0:11]  # 取得表格中1到10格
    result = list()
    result.append((stock_date,) +
                  tuple(td.getText().strip() for td in tds))

    aaaa = 1


def test2():
    import requests
    import json
    import config.proxies_config as proxies_config
    import random

    url = "https://tw.quote.finance.yahoo.net/quote/q"
    now_time = int(datetime.datetime.now().timestamp())
    callback = 'jQuery111306841563040442273_1624119985933'
    engine = SqlAlchemy.get_engine()
    Session = sessionmaker(bind=engine)

    # proxies_list = proxies_config.PROXIES
    # proxies = {
    #     "http": "http://10.10.1.10:3128",
    #     "https": "http://10.10.1.10:1080",
    # }

    error_list = []

    with Session() as session:
        stock_id_list = session.execute("SELECT  distinct  stock_id FROM public.stocks;").fetchall()
        for row in stock_id_list:
            # proxies = random.choice(proxies_list)
            stock_id = row["stock_id"].upper()
            # stock_id = '2499'
            my_params = {'type': 'ta',
                         'perd': 'd',
                         'mkt': '10',
                         'sym': stock_id,
                         'v': '1',
                         'callback': callback,
                         '_': now_time
                         }

            res = requests.get(url, params=my_params)

            print("start================" + stock_id)

            if 200 == res.status_code:
                bbb = res.text
                bbb = bbb.replace(callback + "(", "").replace(");", "")
                try:
                    ccc = json.loads(bbb)
                except Exception as e:
                    error_list.append(stock_id)
                    ccc = {'ta': []}

                ta = ccc["ta"]

                for stock_data in ta:
                    print(stock_data['t'])
                    print(stock_data['o'])
                    print(stock_data['h'])
                    print(stock_data['l'])
                    print(stock_data['c'])
                    print(stock_data['v'])
                    stock_date = stock_data['t']
                    trade_volume = stock_data['v']
                    close_price = stock_data['c']
                    open_price = stock_data['o']
                    highest_price = stock_data['h']
                    lowest_price = stock_data['l']
                    insert_para = dict(stock_date=stock_date,
                                       stock_id=stock_id,
                                       trade_volume=trade_volume,
                                       closing_price=close_price,
                                       opening_price=open_price,
                                       highest_price=highest_price,
                                       lowest_price=lowest_price
                                       )

                    insert_stmt = insert(StockBaseData).values(insert_para)
                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=['stock_date', 'stock_id'],
                        set_=insert_para)

                    session.execute(do_update_stmt)
                session.commit()
            else:
                print("error" + stock_id)

            print(stock_id)
            time.sleep(3)

    print(error_list)


def init():
    from web_crawler import Yahoo
    error_list = []
    engine = SqlAlchemy.get_engine()
    Session = sessionmaker(bind=engine)
    with Session() as session:
        stock_id_list = session.execute("SELECT  distinct  stock_id FROM public.stocks;").fetchall()
        for row in stock_id_list:
            stock_id = row["stock_id"].upper()
            status_code, stock_base_data_model_list = Yahoo.get_stock_data_by_stock_id(stock_id)
            for stock_base_data_model in stock_base_data_model_list:
                if status_code == 200:
                    insert_para = dict(stock_date=stock_base_data_model.stock_date,
                                       stock_id=stock_id,
                                       trade_volume=stock_base_data_model.trade_volume,
                                       closing_price=stock_base_data_model.closing_price,
                                       opening_price=stock_base_data_model.opening_price,
                                       highest_price=stock_base_data_model.highest_price,
                                       lowest_price=stock_base_data_model.lowest_price
                                       )
                    insert_stmt = insert(StockBaseData).values(insert_para)
                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=['stock_date', 'stock_id'],
                        set_=insert_para)

                    session.execute(do_update_stmt)
                error_list.append(stock_id)
            session.commit()
    print(error_list)


if __name__ == '__main__':
    # for ids in newarr:
    #     insert_table(ids)
    #     time.sleep(20)

    # fix_stock("20210619")
    init()
