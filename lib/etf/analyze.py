import os
import constant
import pandas as pd

from lib import logger
log = logger.get_logger()

import streamlit as st

''' Buy at every green and sell at every red '''
def strategy_buy_1d_green_sell_1d_red(df):

    amount_buy = 1000
    amount_to_sell = 1000

    unit_invested = 0
    balance = 0
    trades_buy = 0
    trades_sell = 0

    for _, row in df.iterrows():
        color = row['color']
        etf_price = row['Open']

        if color == 'green':
            unit_bought = amount_buy / etf_price
            unit_invested += unit_bought
            balance -= amount_buy
            trades_buy += 1

        elif color == 'red':
            amount_availaible = min(amount_to_sell, unit_invested * etf_price)
            if amount_availaible == 0:
                continue

            unit_sold = amount_availaible / etf_price
            amount_sold = unit_sold * etf_price

            unit_invested -= unit_sold
            balance += amount_sold

            trades_sell += 1

    balance += unit_invested * etf_price
    stats = {'profit': balance, 'trades_buy': trades_buy, 'trades_sell': trades_sell, 'trades': trades_buy + trades_sell}
    return stats

def find_etf_statistics():
    
    supported_etf = constant.supported_etf

    stats_all = []
    
    for strategy in constant.strategies:

        # Iterate over all ETF to be analyzed
        for etf in supported_etf:        

            # Iterate on each year dataset
            etf_dir = os.path.join(constant.data_dir, "etf", etf.lower())
            for etf_file_path in sorted(os.listdir(etf_dir)):
                year = etf_file_path.split('.')[0]
                etf_file_path = os.path.join(etf_dir, etf_file_path)

                df = pd.read_csv(etf_file_path)
                df['Close_PrevDay'] = df['Close'].shift(1)
                df = df.dropna()
                df['change'] = df.apply(lambda x: (x['Open'] - x['Close_PrevDay']) * 100 /  x['Close_PrevDay'], axis=1)
                df['color'] = df['change'].apply(lambda x: 'green' if x >= 0 else 'red')

                func_name = f"strategy_{strategy}"
                function = globals()[func_name]
                
                stats = {'etf': etf, 'year': year, 'strategy': strategy}
                stats.update(function(df))
                stats_all.append(stats)

    df_stats = pd.DataFrame(stats_all)
    return df_stats