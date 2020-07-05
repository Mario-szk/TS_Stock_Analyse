#! usr/bin/env python
import tushare as ts
import pandas as pd
import TS_getStock
import time

# 从本地读取token
f = open('D:\\股票分析\\token.txt')
token = f.read()

ts.set_token(token)
pro = ts.pro_api()

def get_finIndic(tscode, retry_count=3, pause=2):
    '''
    获取每只股票的财务指标
    ---------
    retry_count:重试次数
    pause:暂停秒数
    '''

    number = 0
    while number <= retry_count:
        try:
            # pd_temp = pro.fina_indicator(ts_code=tscode, period='20191231', fields=
            # 'ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, revenue_ps, extra_item, profit_dedt, gross_margin, current_ratio, quick_ratio,'
            # 'arturn_days, inv_turn, ar_turn, assets_turn, ebit, ebitda, fcff, interestdebt, diluted2_eps, bps, ocfps, cfps, ebit_ps, netprofit_margin, grossprofit_margin,'
            # 'profit_to_gr, saleexp_to_gr, adminexp_of_gr, finaexp_of_gr, impai_ttm, op_of_gr, ebit_of_gr, roe, roe_waa, roe_dt, roa, roe_avg, salescash_to_or,'
            # 'ocf_to_opincome, debt_to_assets, assets_to_eqt, nca_to_assets, currentdebt_to_debt, ebit_to_interest, profit_prefin_exp, non_op_profit, profit_to_op, basic_eps_yoy,'
            # 'dt_eps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, roe_yoy, eqt_yoy, tr_yoy, or_yoy, equity_yoy, rd_exp, update_flag',
            #                           timeout=5)
            pd_temp = pro.fina_indicator(ts_code=tscode, start_date='20170101', end_date='20191231', fields=
             'ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, profit_dedt, current_ratio, quick_ratio,'
             'inv_turn, ar_turn, assets_turn, bps, profit_to_gr, op_of_gr, roe, roe_waa, roe_dt, roa,'
             'salescash_to_or, ocf_to_opincome, debt_to_assets, basic_eps_yoy, dt_eps_yoy, op_yoy, netprofit_yoy, dt_netprofit_yoy,'
             'roe_yoy, tr_yoy, or_yoy, rd_exp, update_flag', timeout=5)

        except:
            number += 1
            if number != retry_count:
                time.sleep(pause)
            else:
                print('自动重试次数超限，未能获取到ts_code代码为%s的股票的财务指标' % tscode)
        else:
            return pd_temp


stock_pd = TS_getStock.get_stock()      # 获取股票列表
stock_finIndic = pd.DataFrame()         # 创建空dataframe，用于存放所有股票的财务指标

for i in stock_pd['ts_code'].values:        # 遍历每只股票的ts_code
    stock_singleFin = get_finIndic(i)       # 获取该只股票的财务指标
    stock_finIndic = stock_finIndic.append(stock_singleFin)      # 将该只股票的财务指标放到汇总dataframe中
    time.sleep(0.75)

# 对财务指标股票表进行去重，保留最新记录 (由于上市公司更新财报，会导致同一公司存在多条记录)
stock_finIndic = stock_finIndic.drop_duplicates(subset=['ts_code', 'end_date'], keep='last')

stock_finIndic.columns = ['ts_code', '公告日期', '报告期', '基本每股收益', '稀释每股收益', '每股营业总收入', '扣除非经常性损益后的净利润', '流动比率', '速动比率', '存货周转率', '应收账款周转率', '总资产周转率',
                  '每股净资产', '净利率(%)', '营业利润率(%)', '净资产收益率(%)', '加权平均净资产收益率(%)', '净资产收益率(扣除非经常性损益)(%)', '总资产报酬率(%)', '销售商品提供劳务收到的现金/营业收入',
                  '经营活动产生的现金流量净额/经营活动净收益', '资产负债率(%)', '基本每股收益同比增长率(%)', '稀释每股收益同比增长率(%)', '营业利润同比增长率(%)', '归属母公司股东的净利润同比增长率(%)',
                  '归属母公司股东的净利润-扣除非经常损益同比增长率(%)', '净资产收益率(摊薄)同比增长率(%)', '营业总收入同比增长率(%)', '营业收入同比增长率(%)', '研发费用', '更新标识']

stock_finIndic.to_csv('D:\\股票分析\\沪深股票财务指标_2017至2019年.csv')





