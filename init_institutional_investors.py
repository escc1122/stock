# -*- coding: utf-8 -*-
"""
Created on Sun May  9 16:36:34 2021

@author: escc1122
"""

from twstock.institutional_investors import InstitutionalInvestors
import customer_db


institutional_investors = InstitutionalInvestors().get(2021,5,10)

if institutional_investors.success==True:
    customer_db.get_connect()
    conn = customer_db.get_connect()
    cursor = conn.cursor()
    datas = institutional_investors.data
    date = institutional_investors.date
    for data in datas:    
        cursor.execute("INSERT INTO public.twse_institutional_investors(stock_date, stock_id, area_investors_buy, area_investors_sell, area_investors_difference, foreign_dealers_buy, foreign_dealers_sell, foreign_dealers_difference, securities_investment_buy, securities_investment_sell, securities_investment_difference, dealers_difference, dealers_difference_buy, dealers_difference_sell, dealers_difference_difference, dealers_hedge_buy, dealers_hedge_sell, dealers_hedge_difference, total_difference)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (date,data[0],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18]))
    conn.commit()
    cursor.close()
    conn.close()
    