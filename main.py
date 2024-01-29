import os
import time
import shutil
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


''' Functions download All MF meta details and individual URI of each MF in CSV '''
def download_mf_meta_csv():
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
    log.info('Analyzing portfolios')
    df_mf_all = pd.read_csv(constant.mf_all_filepath)

    # df_mf_all.sort_values(by=['Quantity'])
    print(df_mf_all[['fundname', 'Invested In', 'Quantity', '% of Total Holding']])

    # shares having highest holding in funds
    # shares with largest quantity occupied
    # shares with largest moving changes +ve
     

if __name__ == "__main__":

    if not os.path.exists(folder_current_date):
        log.info(f"creating dir - {folder_current_date}")
        os.makedirs(folder_current_date)

    download_portfolios()
    analyze_portfolios()