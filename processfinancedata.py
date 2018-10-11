# coding=utf-8
import tushare as ts
import os
import pandas as pd

#===============================================================================
#     四高股的基本要点是:
#     1.盘小(总股本小于2亿,小于0.8亿的袖珍股更好).
#     2.业绩增长,中报业绩或年报业绩每股收益0.5元以上(1元以上更好).
#     3.每股净资产(最好10元以上),公积金高(3元以上)的品种优先.
#     4.每股现金流为正数.
#===============================================================================

def getHighValue(year,quot):
    #===========================================================================
    # code,代码
    # name,名称
    # industry,所属行业
    # area,地区
    # pe,市盈率
    # outstanding,流通股本(亿)
    # totals,总股本(亿)
    # totalAssets,总资产(万)
    # liquidAssets,流动资产
    # fixedAssets,固定资产
    # reserved,公积金
    # reservedPerShare,每股公积金
    # esp,每股收益
    # bvps,每股净资
    # pb,市净率
    # timeToMarket,上市日期
    # undp,未分利润
    # perundp, 每股未分配
    # rev,收入同比(%)
    # profit,利润同比(%)
    # gpr,毛利率(%)
    # npr,净利润率(%)
    # holders,股东人数
    #===========================================================================
    try:
        os.remove("basics-" + str(year) +"-" + str(quot) + ".csv")
    except OSError:
        pass
    basicsDf = ts.get_stock_basics()
    print(basicsDf.dtypes)
    basicsDf['name'] = basicsDf['name'].astype('str')
    basicsDf['industry'] = basicsDf['industry'].astype('str')
    basicsDf['area'] = basicsDf['area'].astype('str')
    basicsDf.to_csv("basics-" + str(year) +"-" + str(quot) + ".csv", header=list(basicsDf), sep=',', encoding='utf-8', index = True)   
    
    
    
    
    #===========================================================================
    # code,代码
    # name,名称
    # eps,每股收益
    # eps_yoy,每股收益同比(%)
    # bvps,每股净资产
    # roe,净资产收益率(%)
    # epcf,每股现金流量(元)
    # net_profits,净利润(万元)
    # profits_yoy,净利润同比(%)
    # distrib,分配方案
    # report_date,发布日期
    #===========================================================================
    #获取业绩报表数据   
    achievDf = ts.get_report_data(year,quot)
    achievDf['code'] = achievDf['code'].apply(str)
    achievDf.to_csv("achiev-" + str(year) +"-" + str(quot) + ".csv", header=list(achievDf), sep=',', encoding='utf-8', index = False)    
    epsCond = achievDf['eps'] >= 0.5
    bvpsCond = achievDf['bvps'] >= 10
    epcfCond = achievDf['epcf'] >= 0
    achievDfFilter = achievDf.loc[epsCond & bvpsCond & epcfCond]
    achievDfFilter.to_csv('achievFilter.csv', header=list(achievDfFilter), sep=',', encoding='utf-8', index = False)     
    
getHighValue(2018,2)  