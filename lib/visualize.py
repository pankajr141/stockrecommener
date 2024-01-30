import streamlit as st
import pandas as pd
from lib import logger
from lib import analyze

log = logger.get_logger()

def display():
    st.set_page_config(layout="wide")
    
    st.title('Mutual Fund houses portfolio analysis')
    log.info('Analyzing portfolios')
    
    info = {}
    info['df_mf_all'] = analyze.get_df_mf_all(info)
    info['df_mf_meta'] = analyze.get_df_mf_meta(info)

    fundhouses = analyze.list_all_fundhouses(info)
    
    stratery = st.radio('Select stratery for fund house selection',
                        ['AUM', 'Returns', 'ALL', 'Custom'],
                        captions = ["Asset Under Management", "Returns past 3 years", 
                                    "All Availaible funds", "I will choose"],
                        horizontal=True)

    fundhouses_opted = []

    k = 3
    if stratery in ['AUM', 'Returns']:
        k = st.slider('Number of funds to consider', 1, len(fundhouses), (3))
        
    if stratery == 'AUM':
        fundhouses_opted = analyze.get_top_k_fund_by_aum(info, k)
    elif stratery == 'Returns':
        fundhouses_opted = analyze.get_top_k_fund_by_returns(info, year=3, k=k)
    elif stratery == 'ALL':
        fundhouses_opted = fundhouses
    elif stratery == 'Custom':
        fundhouses_opted = st.multiselect('select fundhouses', fundhouses)

    st.write("Fund houses selected: ", fundhouses_opted)

    info['df_mf_all'] = analyze.clean_df(info['df_mf_all'])

    j = st.slider('Number of share to consider', 1, 10, (3))

    # shares having highest holding in funds
    st.header('Shares having highest total holding in funds', divider='rainbow')

    df = analyze.get_top_k_stock_by_investment(info, fundhouses_opted, k=j)
    st.write(df)

    # shares with largest percentage occupied
    st.header('Shares having highest avg percentage holding', divider='rainbow')
    df = analyze.get_top_k_stock_by_avg_holding(info, fundhouses_opted, k=j)
    st.write(df)