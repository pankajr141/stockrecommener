import os
from pathlib import Path
home = str(Path.home())

# mode
download_mode = False

# Filesystem 
data_dir = "data"
download_filepath = os.path.join(home, 'Downloads')
mf_meta_filepath = os.path.join(download_filepath, 'Small_Cap.csv')
mf_href_filepath = os.path.join('data', 'filepath_mf_href.csv')
mf_all_filepath = os.path.join('data', 'mf_all.csv')
driver_gecko_filepath = 'geckodriver'

# URIs
website_uri = 'https://trendlyne.com'
url_mf_direct = "https://trendlyne.com/mutual-fund/mf-all/?category=Small-Cap&plan=Direct"
xpath_mf_meta_direct_csv = '//*[@id="mffilter"]/div/div[4]/div/div[4]/button[2]/span'
xpath_mf_meta_href = '//*[@id="mffilter"]/div/div[4]/div/div[6]/div[1]/div[3]/*/div/div[1]/div/div/a'
xpath_mf_meta_name = '//*[@id="mffilter"]/div/div[4]/div/div[6]/div[1]/div[3]/*/div/div[1]/div/div/a/span'

xpath_mf_csv = '//*[@id="mffunddetail"]/div/div[3]/div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[4]/button/span'

