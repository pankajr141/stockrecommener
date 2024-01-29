import os
import time
import shutil
import streamlit as st
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
from lib import logger
log = logger.get_logger()

import constant
mf_meta_filepath = constant.mf_meta_filepath
mf_href_filepath = constant.mf_href_filepath

from datetime import datetime
current_date = datetime.now().strftime('%Y%m')
folder_current_date = os.path.join(constant.data_dir, current_date)

mf_meta_filepath_local = os.path.join(folder_current_date, os.path.basename(mf_meta_filepath))

def get_filename_from_fundname(fund_name):
    return fund_name.replace(' ', '_') + ".csv"

def initize_browser():
    if not constant.download_mode:
        raise Exception("Download mode disabled")

    # Setting firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    options.binary_location = constant.driver_gecko_filepath

    # Setting firefox profile
    fp = FirefoxProfile()
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("javascript.enabled", True)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/xls;application/xlsx;text/csv")
    options.profile = fp

    driver = webdriver.Firefox(options=options)
    return driver


def download_mf_meta_csv():
    ''' Functions download All MF meta details and individual URI of each MF in CSV '''

    driver = initize_browser()
    driver.get(constant.url_mf_direct)

    log.info(f"current uri: {driver.current_url}, waiting for page to load ...")
    time.sleep(2)
    
    driver.find_element(by=By.XPATH, value=constant.xpath_mf_meta_direct_csv).click()
    if not os.path.exists(mf_meta_filepath):
        driver.quit()
        raise Exception(f"unable to download {mf_meta_filepath}")

    # Copy downloaded file from Downloads folder to data directory
    shutil.copyfile(mf_meta_filepath, mf_meta_filepath_local)

    # Fetch URI details of individual MF and save them in a csv
    log.info("Fetching uri details of individual mutual funds ..")
    elems = driver.find_elements(by=By.XPATH, value=constant.xpath_mf_meta_href)
    hrefs = [elem.get_attribute('href') for elem in elems]

    elems = driver.find_elements(by=By.XPATH, value=constant.xpath_mf_meta_name)
    mfnames = [elem.text for elem in elems]
    df = pd.DataFrame(list(zip(mfnames, hrefs)), columns=['mfname', 'href'])

    log.info(f"saving mf href details - {mf_href_filepath}")
    df.to_csv(mf_href_filepath, index=False)

    driver.quit()

def download_mf_csv(fund_uri, fund_name, fund_filename):
    driver = initize_browser()
    driver.get(fund_uri)

    log.info(f"current uri: {driver.current_url}, waiting for page to load ...")
    time.sleep(2)

    driver.find_element(by=By.XPATH, value=constant.xpath_mf_csv).click()
    mf_filepath = os.path.join(constant.download_filepath, fund_filename)

    if not os.path.exists(mf_filepath):
        driver.quit()
        raise Exception(f"unable to download {mf_filepath}")

    mf_filepath_local = os.path.join(folder_current_date, fund_filename)
    shutil.copyfile(mf_filepath, mf_filepath_local)

    driver.quit()

def download_portfolios():
    if not os.path.exists(mf_meta_filepath_local) or not os.path.exists(mf_href_filepath):
       log.info(f"MF Meta file ({mf_meta_filepath_local}) doesn't exist, hence downloading") 
       download_mf_meta_csv()

    log.info(f"processing MF Details file ({mf_meta_filepath_local})")

    # Below block process meta information and chunk all related details
    df_mf_meta = pd.read_csv(mf_meta_filepath_local)

    # Processing Individual MF
    mf_all = []
    for _, row in pd.read_csv(mf_href_filepath).iterrows():
        try:
            fund_name = row['mfname']
            fund_uri = row['href']

            log.info(f"processing fund {fund_name} - {fund_uri}")
            fund_filename = get_filename_from_fundname(fund_name)
            mf_filepath_local = os.path.join(folder_current_date, fund_filename)

            if not os.path.exists(mf_filepath_local):
                log.info(f"MF file ({mf_filepath_local}) doesn't exist, hence downloading")
                download_mf_csv(fund_uri, fund_name, fund_filename)

            df_mf = pd.read_csv(mf_filepath_local)
            df_mf['fundname'] = fund_name
            mf_all.append(df_mf)
        except Exception as err:
            log.error(err)

    df_mf_all = pd.concat(mf_all, axis=0)
    df_mf_all.to_csv(constant.mf_all_filepath, index=False)
    
    print(df_mf_all)

def analyze_portfolios():
    st.title('Mutual Fund houses portfolio analysis')
    log.info('Analyzing portfolios')
    df_mf_all = pd.read_csv(constant.mf_all_filepath)
    df_mf_meta = pd.read_csv(mf_meta_filepath_local)

    fundhouses = df_mf_all['fundname'].unique().tolist()
    
    stratery = st.radio('Select stratery for fund house selection',
                        ['AUM', 'Returns', 'ALL', 'Custom'],
                        captions = ["Asset Under Management", "Returns past 3 years", 
                                    "All Availaible funds", "I will choose"],
                        horizontal=True)

    fundhouses_opted = []

    if stratery == 'AUM':
        fundhouses_opted = df_mf_meta.sort_values(by=['AUM'], ascending=False)['Fund Name'].tolist()[0:3]
    elif stratery == 'Returns':
        fundhouses_opted = df_mf_meta.sort_values(by=['Returns 3Yr'], ascending=False)['Fund Name'].tolist()[0:3]
    elif stratery == 'ALL':
        fundhouses_opted = fundhouses
    elif stratery == 'Custom':
        fundhouses_opted = st.multiselect('select fundhouses', fundhouses)
    st.write("Fund houses selected: ", fundhouses_opted)

    # df_mf_all['Market Value Latest Price'] = df_mf_all['Market Value Latest Price'].fillna(0).apply(lambda x: int(x))
    # df_mf_all.sort_values(by=['Quantity'])

    for column in df_mf_all.columns.tolist():
        try:
            if column == 'Month Change <br> in Shares %':
                df_mf_all[column] = df_mf_all[column].apply(lambda x: str(x).lower().replace('new', '0'))
            df_mf_all[column] = df_mf_all[column].astype(float)
            df_mf_all[column] = df_mf_all[column].fillna(0)

        except Exception as err:
            pass
    # shares having highest holding in funds
    st.header('Shares having highest total holding in funds', divider='rainbow')

    df_mf_all_ = df_mf_all[df_mf_all['fundname'].isin(fundhouses_opted)]
    df_mf_all_['number_of_funds_opted'] = 1

    df_mf_all_ = df_mf_all_.groupby(['Invested In']).sum().reset_index()
    df_mf_all_ = df_mf_all_.sort_values(by=['Market Value Latest Price'], ascending=False).reset_index().head(3)
    df_mf_all_ = df_mf_all_[['Invested In', 'Sector', 'Market Value Latest Price', 
                             'number_of_funds_opted',
                             '% of Total Holding', 'Month Change <br> in Shares', 
                             'Month Change <br> in Shares %']]

    st.write(df_mf_all_)

    # shares with largest percentage occupied
    st.header('Shares having highest avg percentage holding', divider='rainbow')

    df_mf_all_ = df_mf_all[df_mf_all['fundname'].isin(fundhouses_opted)]

    df_mf_all_ = df_mf_all_[['Invested In', 'Sector', 'Market Value Latest Price', '% of Total Holding', 'Month Change <br> in Shares', 
                             'Month Change <br> in Shares %']]
    df_mf_all_ = df_mf_all_.groupby(['Invested In', 'Sector']).mean().reset_index()
    df_mf_all_ = df_mf_all_.sort_values(by=['% of Total Holding'], ascending=False).reset_index().head(3)

    st.write(df_mf_all_)

    # shares with largest moving changes +ve 

if __name__ == "__main__":

    if not os.path.exists(folder_current_date):
        log.info(f"creating dir - {folder_current_date}")
        os.makedirs(folder_current_date)

    #download_portfolios()
    analyze_portfolios()
