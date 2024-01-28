import os
import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

import logger
log = logger.get_logger()

import constant
mf_details_filepath = constant.mf_details_filepath

def initize_browser():

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

def download_mf_direct_csv():
    driver = initize_browser()
    driver.get(constant.url_mf_direct)

    log.info(f"current uri: {driver.current_url}, waiting for page to load ...")
    time.sleep(2)
    
    driver.find_element(by=By.XPATH, value=constant.xpath_mf_direct_csv).click()
    if not os.path.exists(mf_details_filepath):
        driver.quit()
        raise Exception(f"unable to download {mf_details_filepath}")

    driver.quit()

def process():
    if not os.path.exists(mf_details_filepath):
       log.info(f"MF Details file ({mf_details_filepath}) doesn't exist, hence downloading") 
       download_mf_direct_csv()

    log.info(f"processing MF Details file ({mf_details_filepath})")

    df_mfdirect = pd.read_csv(mf_details_filepath)
    print(df_mfdirect)
    
if __name__ == "__main__":
    process()