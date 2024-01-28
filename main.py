import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver



def download(binary=None):
    from selenium import webdriver
    driver = webdriver.Firefox()
    driver.get('http://google.com')
    print(driver.title)
    driver.quit()


    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.manager.showWhenStarting", False)

    options = FirefoxOptions()
    driver = webdriver.Firefox(firefox_profile=fp, firefox_options=options, executable_path=binary)
    driver.get("https://www.iexindia.com/marketdata/market_snapshot.aspx")
    driver.quit()


binary = "geckodriver"
download(binary)