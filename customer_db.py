# -*- coding: utf-8 -*-
"""
Created on Sun May  2 14:46:21 2021

@author: escc1122
"""

import psycopg2
import config

# Update connection string information
host = config.DB_HOST
dbname = config.DB_NAME
user = config.DB_USER
password = config.DB_PASSWORD

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS stocks_classification (classification_id VARCHAR(10) PRIMARY KEY, classification_name VARCHAR(50));")
cursor.execute("CREATE TABLE IF NOT EXISTS stocks (stock_id VARCHAR(10),classification_id VARCHAR(10) , stock_name VARCHAR(50),PRIMARY KEY (stock_id, classification_id));")
cursor.execute("CREATE TABLE IF NOT EXISTS yestoday_stock_status (stock_id VARCHAR(10) PRIMARY KEY, trade_volume bigint, close_price real);")



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
    cursor.execute("select stock_id,trade_volume,close_price from public.yestoday_stock_status WHERE trade_volume>0 and close_price>0;")
    rows = cursor.fetchall()
    
    # Print all rows
    for row in rows:
        t = {}
        t['trade_volume'] = row[1]
        t['close_price'] = row[2]
        return_map[row[0]]=t
    return return_map


    
    
    

