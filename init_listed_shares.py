# -*- coding: utf-8 -*-
"""
初始化上市股票資料
"""

import customer_db
import datetime
import requests
import time

classification = {
    "01": "水泥工業"
    , "02": "食品工業"
    , "03": "塑膠工業"
    , "04": "紡織纖維"
    , "05": "電機機械"
    , "06": "電器電纜"
    , "07": "化學生技醫療"
    , "21": "化學工業"
    , "22": "生技醫療業"
    , "08": "玻璃陶瓷"
    , "09": "造紙工業"
    , "10": "鋼鐵工業"
    , "11": "橡膠工業"
    , "12": "汽車工業"
    , "13": "電子工業"
    , "24": "半導體業"
    , "25": "電腦及週邊設備業"
    , "26": "光電業"
    , "27": "通信網路業"
    , "28": "電子零組件業"
    , "29": "電子通路業"
    , "30": "資訊服務業"
    , "31": "其他電子業"
    , "14": "建材營造"
    , "15": "航運業"
    , "16": "觀光事業"
    , "17": "金融保險"
    , "18": "貿易百貨"
    , "23": "油電燃氣業"
    , "19": "綜合"
    , "20": "其他"
}


def init_stocks_classification():
    customer_db.get_connect()
    conn = customer_db.get_connect()
    cursor = conn.cursor()
    for k in classification:
        cursor.execute(
            "INSERT INTO stocks_classification (classification_id, classification_name) VALUES (%s, %s) on conflict (classification_id) do nothing;",
            (k, classification[k]))

    conn.commit()
    cursor.close()
    conn.close()


def init_stocks(classification_id):
    print("classification_id : " + classification_id)
    now_time = int(datetime.datetime.now().timestamp())
    url = "https://www.twse.com.tw/zh/api/codeFilters"
    my_params = {'filter': classification_id, '_': now_time}
    r = requests.get(url, params=my_params)
    data = r.json()
    customer_db.get_connect()
    conn = customer_db.get_connect()
    cursor = conn.cursor()
    for k in data["resualt"]:
        print(k.split("\t")[0] + " " + k.split("\t")[1])
        cursor.execute(
            "INSERT INTO stocks (stock_id, classification_id, stock_name) VALUES (%s, %s, %s) on conflict (stock_id,classification_id) do nothing;",
            (k.split("\t")[0], classification_id, k.split("\t")[1]))
    conn.commit()
    cursor.close()
    conn.close()


init_stocks_classification()
for k in classification:
    init_stocks(k)
    time.sleep(5)
