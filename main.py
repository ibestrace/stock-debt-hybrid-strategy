import pandas as pd
import akshare as ak
import quantstats as qs

def GetFundInfoByAkshare(fund, indicator):
    fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund=fund, indicator=indicator)
    return fund_open_fund_info_em_df

def FormatData(fund_open_fund_info_em_df):
    data = fund_open_fund_info_em_df
    data.rename(columns={'净值日期':'date', '累计净值':'cumvalue'}, inplace=True)
    data.date = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    cumvalue = pd.Series(data.cumvalue)
    return cumvalue

fund_open_fund_info_em_df = GetFundInfoByAkshare(fund='000082', indicator="累计净值走势")
cumvalue = FormatData(fund_open_fund_info_em_df)
returns = cumvalue.pct_change().dropna()
qs.reports.html(returns=cumvalue,
                output='data',
                title='嘉实',
                download_filename='嘉实12.html')