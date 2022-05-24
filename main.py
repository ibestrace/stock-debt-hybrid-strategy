import pandas as pd
import akshare as ak
import quantstats as qs
from IPython.display import display

fund_name_em_df = ak.fund_name_em()
equity_fund_df = fund_name_em_df[fund_name_em_df['基金类型'] == '股票型'].loc[:, ['基金代码', '基金简称']]

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

fund_matrix = equity_fund_df.reset_index()
fund_matrix.drop('index',axis=1, inplace=True)
fund_matrix.rename(columns={'基金代码':'fund_code', '基金简称':'fund_abb'}, inplace=True)

for index in fund_matrix.index:
    fund = fund_matrix.loc[index, 'fund_code']
    fund_open_fund_info_em_df = GetFundInfoByAkshare(fund=fund, indicator="累计净值走势")
    cumvalue = FormatData(fund_open_fund_info_em_df)
    returns = cumvalue.pct_change().dropna()
    sharpe_ratio = qs.stats.sharpe(returns=returns)
    sortino_ratio = qs.stats.sortino(returns=returns)
    max_drawdown = qs.stats.max_drawdown(cumvalue)
    var = qs.stats.var(returns=returns)
    cvar = qs.stats.cvar(returns=returns)
    volatility = qs.stats.volatility(returns=returns)
    fund_matrix.loc[index, 'sharpe'] = sharpe_ratio
    fund_matrix.loc[index, 'sortino'] = sortino_ratio
    fund_matrix.loc[index, 'max_drawdown'] = max_drawdown
    fund_matrix.loc[index, 'var'] = var
    fund_matrix.loc[index, 'cvar'] = cvar
    fund_matrix.loc[index, 'volatility'] = volatility

fund_matrix.dropna(inplace=True)
fund_matrix.to_excel('data/fund_matrix.xlsx')

fund_matrix = pd.read_excel('data/fund_matrix.xlsx',
                            usecols=['fund_code','fund_abb'],
                            dtype={'fund_code':str})

for index in fund_matrix.index:
    fund = fund_matrix.loc[index, 'fund_code']
    fund_open_fund_info_em_df = GetFundInfoByAkshare(fund=fund, indicator="累计净值走势")
    cumvalue = FormatData(fund_open_fund_info_em_df)
    returns = cumvalue.pct_change().dropna()
    qs.reports.html(returns=cumvalue,
                    output='E:\\Project\\portfolioanalysis\\stock-debt-hybrid-strategy\\data\\',
                    title=fund_matrix.loc[index, 'fund_abb'] + '概览',
                    download_filename=fund_matrix.loc[index, 'fund_abb'] + '概览.html')