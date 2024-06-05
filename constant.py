import os
from pathlib import Path
from datetime import datetime

home = str(Path.home())

# Global
download_mode = True
driver_gecko_filepath = 'geckodriver'

# Filesystem 
data_dir = "data"
download_filepath = os.path.join(home, 'Downloads')
folder_current_date = os.path.join(data_dir, datetime.now().strftime('%Y%m'))


# mutual funds based recommendation
mf_meta_filepath = os.path.join(download_filepath, 'Small_Cap.csv')
mf_href_filepath = os.path.join('data', 'filepath_mf_href.csv')
mf_all_filepath = os.path.join('data', 'mf_all.csv')
mf_meta_filepath_local = os.path.join(folder_current_date, os.path.basename(mf_meta_filepath))
mf_all_filepath_local = os.path.join(data_dir, os.path.basename(mf_all_filepath))


# URIs
website_uri = 'https://trendlyne.com'
url_mf_direct = "https://trendlyne.com/mutual-fund/mf-all/?category=Small-Cap&plan=Direct"
xpath_mf_meta_direct_csv = '//*[@id="mffilter"]/div/div[4]/div/div[4]/button[2]/span'
xpath_mf_meta_href = '//*[@id="mffilter"]/div/div[4]/div/div[6]/div[1]/div[3]/*/div/div[1]/div/div/a'
xpath_mf_meta_name = '//*[@id="mffilter"]/div/div[4]/div/div[6]/div[1]/div[3]/*/div/div[1]/div/div/a/span'
xpath_mf_csv = '//*[@id="mffunddetail"]/div/div[3]/div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[4]/button/span'


# ETF based recommendation
supported_etf = ["NSEI"]
strategies = ["buy_1d_green_sell_1d_red"]