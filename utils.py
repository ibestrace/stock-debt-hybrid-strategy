'''
搭建量化研究函数库
'''
#导入必备的库
import pandas as pd
import akshare as ak

# 通过基金代码读取基金的历史净值
def GetFundInfoByAkshare(fund, indicator):
    fund_open_fund_info_em_df = ak.fund_open_fund_info_em(fund=fund, indicator=indicator)
    return fund_open_fund_info_em_df

# 格式化基金的历史净值
def FormatData(fund_open_fund_info_em_df):
    data = fund_open_fund_info_em_df
    data.rename(columns={'净值日期':'date', '累计净值':'cumvalue'}, inplace=True)
    data.date = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    cumvalue = pd.Series(data.cumvalue)
    return cumvalue

