import os
from pathlib import Path
home = str(Path.home())

driver_gecko_filepath = 'geckodriver'

url_mf_direct = "https://trendlyne.com/mutual-fund/mf-all/?category=Small-Cap&plan=Direct"
xpath_mf_direct_csv = '//*[@id="mffilter"]/div/div[4]/div/div[4]/button[2]/span'

mf_details_filepath = os.path.join(home, 'Downloads', 'Small_Cap.csv')