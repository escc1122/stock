# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:06:27 2021

@author: escc1122
"""
import sys
import traceback
import abc


class RuntimeStockData():
    def __init__(self, id, stocks):
        # 盤中交易量
        self._accumulate_trade_volume = int(0)
        # 盤中最高股價
        self._high = int(0)
        # 股票id
        self._stock_id = id
        self._name = ''
        self.__latest_trade_price = float(0)
        self.__trade_price = float(0)
        try:
            if id in stocks:
                realtime = stocks[id]['realtime']
                best_bid_price = realtime['best_bid_price']
                best_ask_price = realtime['best_ask_price']
                self._name = stocks[id]['info']['name']
                self._accumulate_trade_volume = int(realtime['accumulate_trade_volume'])
                self._high = float(realtime['high'])
                self.__latest_trade_price = float(realtime['latest_trade_price'])
                if best_bid_price[0] == '-':
                    self.__trade_price = float(best_ask_price[0])
                else:
                    self.__trade_price = float(best_bid_price[0])
            else:
                print("id no found id : {}", id)
        except:
            print("An exception occurred id : " + id)
            print("An exception occurred accumulate_trade_volume : {} : ", realtime['accumulate_trade_volume'])
            print("An exception occurred high: {} : ", realtime['high'])

    @property
    def accumulate_trade_volume(self):
        return self._accumulate_trade_volume

    @accumulate_trade_volume.setter
    def accumulate_trade_volume(self, new_data):
        self._accumulate_trade_volume = new_data

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, new_data):
        self._high = new_data

    @property
    def stock_id(self):
        return self._stock_id

    @stock_id.setter
    def stock_id(self, new_data):
        self._stock_id = new_data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_data):
        self._name = new_data

    @property
    def latest_trade_price(self):
        return self.__latest_trade_price

    @latest_trade_price.setter
    def latest_trade_price(self, new_data):
        self.__latest_trade_price = new_data

    @property
    def trade_price(self):
        return self.__trade_price

    @trade_price.setter
    def trade_price(self, new_data):
        self.__trade_price = new_data


class ICondition(abc.ABC):
    @abc.abstractmethod
    def check(self, runtime_stock_data):
        pass

    # @abc.abstractmethod
    # def get_send_message(self):
    #     pass

    @abc.abstractmethod
    def clean_message(self):
        pass


class Conditions(ICondition):
    def __init__(self):
        self.__conditions = []

    def addCondition(self, condition):
        self.__conditions.append(condition)

    def check(self, runtime_stock_data):
        for condition in self.__conditions:
            condition.check(runtime_stock_data)

    def clean_message(self):
        for condition in self.__conditions:
            condition.clean_message()

    @property
    def conditions(self):
        return self.__conditions


class Condition(ICondition):
    def __init__(self, yestoday_stock_status):
        # 昨日收盤資料
        self._yestoday_stock_status = yestoday_stock_status
        self._no_seed_stock_id = []
        self._send_message = ''
        self._send_message_title = ''

    def check(self, runtime_stock_data):
        pass

    def get_send_message(self):
        msg = ''
        # print("_send_message_title : " + self._send_message_title)
        if not self._send_message == '':
            msg = self._send_message_title + self._send_message
        return msg

    def clean_message(self):
        self._send_message = ''


class PriceAndVolumeCondition(Condition):
    def __init__(self, yestoday_stock_status, securities_investment_buy_three_day_dict, price_market=1.03,
                 volume_market=2):
        super().__init__(yestoday_stock_status)
        self._price_market = price_market
        self._volume_market = volume_market
        self.__send_message_list = []
        self.__securities_investment_keys = securities_investment_buy_three_day_dict.keys()
        self._send_message_title = "<code>漲幅超過 {} ,交易量超過 {}</code>\n".format("{:.2%}".format(price_market - 1),
                                                                             "{:.0%}".format(volume_market))

    def __sort(self):
        pass

    def get_send_message(self):
        send_message = ''
        msg = ''
        self.__send_message_list.sort(key=lambda one_data: one_data[3], reverse=True)
        for one_data in self.__send_message_list:
            id = one_data[0]
            send_message = send_message + "<code>{} :{},交易量:{},漲幅{}</code>\n".format(id, one_data[1],
                                                                                     "{:.0%}".format(one_data[3]),
                                                                                     "{:.2%}".format(one_data[2] - 1))
            if id in self.__securities_investment_keys:
                send_message = send_message + "<code>===={}投信連三買=====</code>\n".format(id)
        if not send_message == '':
            msg = self._send_message_title + send_message
        return msg

    def clean_message(self):
        self._send_message = ''
        self.__send_message_list = []

    def set_condition_price_and_volume_market(self, price_market=1.03, volume_market=2):
        self._price_market = price_market
        self._volume_market = volume_market
        self._send_message_title = "<code>漲幅超過 {} , 交易量超過 {} 倍</code>\n".format("{:.2%}".format(price_market - 1),
                                                                                "{:.0%}".format(volume_market))

    def check(self, runtime_stock_data):
        # send_message = ''
        id = ''
        try:
            id = runtime_stock_data.stock_id
            accumulate_trade_volume = runtime_stock_data.accumulate_trade_volume
            trade_price = runtime_stock_data.trade_price
            name = runtime_stock_data.name
            yestoday_trade_volum = int(self._yestoday_stock_status[id]['trade_volume'])
            yestoday_close_price = float(self._yestoday_stock_status[id]['close_price'])
            runtime_price_market = trade_price / yestoday_close_price
            runtime_volume_market = accumulate_trade_volume / yestoday_trade_volum
            if id not in self._no_seed_stock_id and runtime_price_market >= self._price_market and runtime_volume_market >= self._volume_market:
                self._no_seed_stock_id.append(id)
                self.__send_message_list.append([id, name, runtime_price_market, runtime_volume_market])
        except Exception as e:
            print("check error occurred id : " + id)
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)


# 投信連買3天   
class SecuritiesInvestmentCondition(Condition):
    def __init__(self, yestoday_stock_status, securities_investment_buy_three_day_dict, price_market=1.03):
        super().__init__(yestoday_stock_status)
        self.__securities_investment_buy_three_day_dict = securities_investment_buy_three_day_dict
        self.__securities_investment_keys = securities_investment_buy_three_day_dict.keys()
        self._price_market = price_market
        self.__send_message_list = []
        self._send_message_title = "<code>al_test漲幅超過 {} ,投信三天連買</code>\n".format("{:.2%}".format(price_market - 1))

    def __sort(self):
        pass

    def get_send_message(self):
        send_message = ''
        msg = ''
        self.__send_message_list.sort(key=lambda one_data: one_data[3], reverse=True)
        for one_data in self.__send_message_list:
            send_message = send_message + "<code>{} :{},三天交易量:{},漲幅{}</code>\n".format(one_data[0], one_data[1],
                                                                                       one_data[3],
                                                                                       "{:.2%}".format(one_data[2] - 1))
        if not send_message == '':
            msg = self._send_message_title + send_message
        return msg

    def clean_message(self):
        self._send_message = ''
        self.__send_message_list = []

    def check(self, runtime_stock_data):
        id = ''
        try:
            id = runtime_stock_data.stock_id
            # accumulate_trade_volume = runtime_stock_data.accumulate_trade_volume
            trade_price = runtime_stock_data.trade_price
            name = runtime_stock_data.name
            # yestoday_trade_volum = int(self._yestoday_stock_status[id]['trade_volume'])
            yestoday_close_price = float(self._yestoday_stock_status[id]['close_price'])
            runtime_price_market = trade_price / yestoday_close_price
            if id not in self._no_seed_stock_id and id in self.__securities_investment_keys and runtime_price_market >= self._price_market:
                self._no_seed_stock_id.append(id)
                self.__send_message_list.append(
                    [id, name, runtime_price_market, self.__securities_investment_buy_three_day_dict[id]])
        except Exception as e:
            print("check error occurred id : " + id)
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
