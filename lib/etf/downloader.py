import os
import constant
from datetime import datetime
import yfinance as yf

from lib import logger
log = logger.get_logger()

# Download historical Nifty 50 data

def download_etf_data():

    supported_etf = constant.supported_etf
    for etf in supported_etf:
        
        etf_dir = os.path.join(constant.data_dir, "etf", etf.lower())
        if not os.path.exists(etf_dir):
            os.makedirs(etf_dir)

        startyear = 1980
        current_year = datetime.now().year
        for year in range(startyear, current_year + 1):
            etf_download_path = os.path.join(etf_dir, f"{year}.csv")
            if year != current_year and os.path.exists(etf_download_path):
                log.info(f"skipping {etf} : {year} as {etf_download_path} already exists ...")
            download_etf_yearly_data(etf, year, etf_download_path)

def download_etf_yearly_data(etf, year, etf_download_path):
    log.info(f"Downloading {etf} : {year} -> {etf_download_path} ...")

    df = yf.download("^NSEI", start=f"{year}-01-01", end=f"{year}-12-31").reset_index()
    if df.shape[0]:
        df.to_csv(etf_download_path, index=False)

if __name__ == "__main__":
    download_etf_data()