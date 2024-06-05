import constant
import pandas as pd

def get_df_mf_all(info):
    if 'df_mf_all' in info.keys():
        return info['df_mf_all']

    df = pd.read_csv(constant.mf_all_filepath_local)
    return df

def get_df_mf_meta(info={}):
    if 'df_mf_meta' in info.keys():
        return info['df_mf_meta']

    df = pd.read_csv(constant.mf_meta_filepath_local)
    return df

def clean_df(df):
    for column in df.columns.tolist():
        try:
            if column == 'Month Change <br> in Shares %':
                df[column] = df[column].apply(lambda x: str(x).lower().replace('new', '0'))
            df[column] = df[column].astype(float)
            df[column] = df[column].fillna(0)

        except Exception as err:
            pass
    return df

def list_all_fundhouses(info={}):
    df = get_df_mf_all(info)
    fundhouses = df['fundname'].unique().tolist()
    return fundhouses

def get_top_k_fund_by_aum(info={}, k=3):
    df = get_df_mf_meta(info)
    fundhouses = df.sort_values(by=['AUM'], ascending=False)['Fund Name'].tolist()[0:k]
    return fundhouses

def get_top_k_fund_by_returns(info={}, year=3, k=3):
    df = get_df_mf_meta(info)

    key = 'Returns 3Yr'
    if year == 5:
        key = 'Returns 5Yr'
    elif year == 1:
        key = 'Returns 1Yr'

    fundhouses = df.sort_values(by=[key], ascending=False)['Fund Name'].tolist()[0:k]
    return fundhouses


def get_top_k_stock_by_investment(info, fundhouses, k=3):
    df = get_df_mf_all(info)
    df = df[df['fundname'].isin(fundhouses)]
    df['number_of_funds_opted'] = 1
    df['Market Value Latest Price'] = df['Market Value Latest Price'].apply(lambda x: int(x))

    df = df.groupby(['Invested In']).agg({'Sector': lambda x: x.iloc[0], 
                                          'Market Value Latest Price': 'sum', 
                                          'number_of_funds_opted': 'count', 
                                          '% of Total Holding': 'sum', 
                                          'Month Change <br> in Shares': 'sum', 
                                          'Month Change <br> in Shares %': 'sum'})

    for col in ['% of Total Holding', 'Month Change <br> in Shares %']:
        df[col] = df[col] / len(fundhouses)
    df = df.sort_values(by=['Market Value Latest Price'], ascending=False).reset_index().head(k)
    return df

def get_top_k_stock_by_avg_holding(info, fundhouses, k=3):
    df = get_df_mf_all(info)
    df = df[df['fundname'].isin(fundhouses)]
    df['number_of_funds_opted'] = 1
    df['Market Value Latest Price'] = df['Market Value Latest Price'].apply(lambda x: int(x))

    df = df.groupby(['Invested In']).agg({'Sector': lambda x: x.iloc[0], 
                                          'Market Value Latest Price': 'sum', 
                                          'number_of_funds_opted': 'count', 
                                          '% of Total Holding': 'sum', 
                                          'Month Change <br> in Shares': 'sum', 
                                          'Month Change <br> in Shares %': 'sum'})
    for col in ['% of Total Holding', 'Month Change <br> in Shares %']:
        df[col] = df[col] / len(fundhouses)
    df = df.sort_values(by=['% of Total Holding'], ascending=False).reset_index().head(k)
    return df