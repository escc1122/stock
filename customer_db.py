# -*- coding: utf-8 -*-
"""
Created on Sun May  2 14:46:21 2021

@author: escc1122
"""

import psycopg2
import config.db_config as config
from sqlalchemy import create_engine

# Update connection string information
host = config.DB_HOST
dbname = config.DB_NAME
user = config.DB_USER
password = config.DB_PASSWORD

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS stocks_classification (classification_id VARCHAR(10) PRIMARY KEY, classification_name VARCHAR(50));")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS stocks (stock_id VARCHAR(10),classification_id VARCHAR(10) , stock_name VARCHAR(50),PRIMARY KEY (stock_id, classification_id));")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS yestoday_stock_status (stock_id VARCHAR(10) PRIMARY KEY, trade_volume bigint, close_price real, open_price real);")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS public.twse_institutional_investors(stock_date character varying(8) NOT NULL,stock_id character varying(10) NOT NULL,area_investors_buy bigint,area_investors_sell bigint,area_investors_difference bigint,foreign_dealers_buy bigint,foreign_dealers_sell bigint,foreign_dealers_difference bigint,securities_investment_buy bigint,securities_investment_sell bigint,securities_investment_difference bigint,dealers_difference bigint,dealers_difference_buy bigint,dealers_difference_sell bigint,dealers_difference_difference bigint,dealers_hedge_buy bigint,dealers_hedge_sell bigint,dealers_hedge_difference bigint,total_difference bigint,PRIMARY KEY (stock_date, stock_id));")

conn.commit()
cursor.close()
conn.close()


def get_connect():
    conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
    conn = psycopg2.connect(conn_string)
    return conn


def get_stock_ids():
    return_array = []
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT distinct stock_id FROM public.stocks;")
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        return_array.append(row[0])
    return return_array


def get_yestoday_stock_status():
    return_map = {}
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute(
        "select stock_id,trade_volume,close_price from public.yestoday_stock_status WHERE trade_volume>0 and close_price>0;")
    rows = cursor.fetchall()

    # Print all rows
    for row in rows:
        t = {'trade_volume': row[1], 'close_price': row[2]}
        return_map[row[0]] = t
    return return_map


def get_securities_investment_buy_three_day_dict():
    return_map = {}
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT stock_id,sum(securities_investment_difference) as total FROM public.twse_institutional_investors where stock_date in (select stock_date from twse_institutional_investors where stock_id='2330' order by stock_date desc limit 3) AND securities_investment_difference>0 group by stock_id having count(stock_id)=3")
    rows = cursor.fetchall()

    for row in rows:
        return_map[row[0]] = int(row[1])
    return return_map


# def get_engine():
#     db_string = "postgresql+psycopg2://{0}:{1}@{2}:5432/{3}".format(user, password, host, dbname)
#     engine = create_engine(db_string,
#                            max_overflow=0,  # 超過連線池大小外最多建立的連線
#                            pool_size=5,  # 連線池大小
#                            pool_timeout=30,  # 池中沒有執行緒最多等待的時間，否則報錯
#                            pool_recycle=-1,  # 多久之後對執行緒池中的執行緒進行一次連線的回收（重置）
#                            echo=True)
#     return engine



try:
    from synchronize import make_synchronized
except ImportError:
    def make_synchronized(func):
        import threading
        func.__lock__ = threading.Lock()

        # 用裝飾器實現同步鎖
        def synced_func(*args, **kwargs):
            with func.__lock__:
                return func(*args, **kwargs)

        return synced_func


class SqlAlchemy:
    __db_string = "postgresql+psycopg2://{0}:{1}@{2}:5432/{3}".format(user, password, host, dbname)
    __engine = None

    @classmethod
    @make_synchronized
    def get_engine(cls):
        if cls.__engine is None:
            cls.__engine = create_engine(cls.__db_string,
                                         max_overflow=0,  # 超過連線池大小外最多建立的連線
                                         pool_size=5,  # 連線池大小
                                         pool_timeout=30,  # 池中沒有執行緒最多等待的時間，否則報錯
                                         pool_recycle=-1,  # 多久之後對執行緒池中的執行緒進行一次連線的回收（重置）
                                         echo=True)
        return cls.__engine
