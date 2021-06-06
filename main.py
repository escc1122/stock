# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:19:30 2021

@author: escc1122
"""
import twstock
import customer_db
import numpy as np
import time
from twstock.proxy import RoundRobinProxiesProvider
import config.proxies_config as proxies_config
import condition
from util.utils import Utils


def main():
    proxies = proxies_config.PROXIES

    rrpr = RoundRobinProxiesProvider(proxies)
    twstock.proxy.configure_proxy_provider(rrpr)

    yestoday_stock_status = customer_db.get_yestoday_stock_status()

    yestoday_stock_status_keys = yestoday_stock_status.keys()

    securities_investment_buy_three_day_dict = customer_db.get_securities_investment_buy_three_day_dict()

    count = 0

    # 條件 start
    conditions = condition.Conditions()
    # 盤中漲幅超過 3% , 交易量超過 2 倍
    condition_2 = condition.PriceAndVolumeCondition(yestoday_stock_status, securities_investment_buy_three_day_dict,
                                                    1.03,
                                                    2)

    condition_3 = condition.SecuritiesInvestmentCondition(yestoday_stock_status,
                                                          securities_investment_buy_three_day_dict,
                                                          1.03)

    # conditions.add_condition(condtion1)
    conditions.add_condition(condition_2)
    conditions.add_condition(condition_3)

    # 條件 end

    while 1:
        print(count)
        count = count + 1
        stock_array = []
        for stock_id in yestoday_stock_status_keys:
            stock_array.append(stock_id)

        # test
        # stock_array = ["2615","2537","3059","4952"]
        newarr = np.array_split(stock_array, int(len(stock_array) / 150) + 1)

        for ids in newarr:
            # print(ids)
            stocks = {}
            try:
                stocks = twstock.realtime.get(ids.tolist())
            except:
                stocks['success'] = False
                print("twstock.realtime.get error")
            # stocks = twstock.realtime.get(ids.tolist())
            if stocks['success']:
                localtime = time.localtime()
                result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
                print('True ' + result)
                for id in ids:
                    try:
                        runtime_stock_data = condition.RuntimeStockData(id, stocks)
                        conditions.check(runtime_stock_data)
                    except Exception as e:
                        Utils.deal_with_exception(e, "An exception occurred id : " + id)
            else:
                print('http error')

            conditions.send_message()
            conditions.clean_message()
            time.sleep(20)


if __name__ == '__main__':
    main()
