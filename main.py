# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:19:30 2021

@author: escc1122
"""
import twstock
import customer_db
import numpy as np
import time
import requests
from twstock.proxy import RoundRobinProxiesProvider
import config
import sys
import traceback


def send_msg(send_message):
    print(send_message)
    if not send_message=='':            
        url = config.TELEGRAM_BOT_URL+"sendMessage"
        my_params = {'chat_id': config.TELEGRAM_BOT_CHAT_ID, 
                          'parse_mode': 'html',
                          'text':send_message
                          }
            
        r = requests.get(url,params =my_params)
        data = r.json()
        

proxies = config.PROXIES

rrpr = RoundRobinProxiesProvider(proxies)
twstock.proxy.configure_proxy_provider(rrpr)

yestoday_stock_status = customer_db.get_yestoday_stock_status()

yestoday_stock_status_keys = yestoday_stock_status.keys()

count=0

while 1:
    print(count)
    count = count+1
    stock_array = []
    send_stock_array =[]
    for stock_id in yestoday_stock_status_keys:
        stock_array.append(stock_id)
        
    
    newarr = np.array_split(stock_array, int(len(stock_array)/100))
    # newarr = np.array_split(stock_array, 1)
    
    for ids in newarr:
        send_message=''
        try:
            stocks = twstock.realtime.get(ids.tolist())
            if stocks['success'] == True:
                print('True')
                for id in ids:
                    realtime = stocks[id]['realtime']
                    name = stocks[id]['info']['name']
                    accumulate_trade_volume = int(realtime['accumulate_trade_volume'])
                    yestoday_trade_volum = int(yestoday_stock_status[id]['trade_volume'])
                    yestoday_close_price = float(yestoday_stock_status[id]['close_price'])
                    high = float(realtime['high'])
                    if high/yestoday_close_price>1.03 and accumulate_trade_volume/yestoday_trade_volum>=2:
                        send_stock_array.append(id)
                        send_message = send_message + "<code>" + id + " : " + name + "</code>\n"
            else:
                print('http error')
        except Exception as e:
            print("An exception occurred")
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)

           
        
        send_msg(send_message)
        time.sleep(20)
        break #out
    
    

    if len(send_stock_array)>0:
        for key in send_stock_array:
            del yestoday_stock_status[key]
            print(key)
        
        # url = "https://api.telegram.org/bot1647749192:AAHarEJBgOWYP5km-RchwC7wufVAsxEYarQ/sendMessage"
        # my_params = {'chat_id': -505021928, 
        #               'parse_mode': 'html',
        #               'text':send_message
        #               }
        
        # r = requests.get(url,params =my_params)
        # data = r.json()
        
