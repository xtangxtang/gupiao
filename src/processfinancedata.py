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

def getHighValue(year,quot, refresh=1):
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
    basicFilePath = "..//basics-" + str(year) +"-" + str(quot) + ".xlsx"
    
    if refresh:
        try:
            os.remove(basicFilePath)
        except OSError:
            pass     
    
    basicFileHeader = ['代码','名称','所属行业','地区','市盈率','流通股本(亿)','总股本(亿)','总资产(万)','流动资产','固定资产',
                       '公积金','每股公积金','每股收益','每股净资','市净率','上市日期','未分利润','每股未分配','收入同比(%)','利润同比(%)',
                       '毛利率(%)','净利润率(%)','股东人数']    
    
    if os.path.isfile(basicFilePath):
        basicsDf = pd.read_excel(basicFilePath, index_col=False,encoding='utf-8')
        basicsDf['代码'] = basicsDf['代码'].astype('str')
        basicsDf['代码'] = basicsDf['代码'].apply(lambda x: x.zfill(6))
    else:
        basicsDf = ts.get_stock_basics()    
        basicsDf.reset_index(level=0, inplace=True)
        basicsDf['code'] = basicsDf['code'].apply(lambda x: x.zfill(6))
        basicsDf['code'] = basicsDf['code'].astype('str')
        basicsDf['name'] = basicsDf['name'].astype('str')
        basicsDf['industry'] = basicsDf['industry'].astype('str')
        basicsDf['area'] = basicsDf['area'].astype('str')        
        basicsDf.to_excel(basicFilePath, header=list(basicFileHeader), encoding='utf-8', index = False)   
    
    basicsFilterFilePath = "..//basics-filter-" + str(year) +"-" + str(quot) + ".xlsx"
    totalCond = basicsDf['总股本(亿)'] <= 2
    espCond = basicsDf['每股收益'] >= 0.5
    bvpsCond = basicsDf['每股净资'] >= 10
    reservedPerShareCond = basicsDf['每股公积金'] >= 3
    basicsDfFilter = basicsDf.loc[totalCond & espCond & bvpsCond & reservedPerShareCond]    
    basicsDfFilter.to_excel(basicsFilterFilePath, header=list(basicFileHeader), encoding='utf-8', index = False)   
    
    
    
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
    achievFilePath = "..//achiev-" + str(year) +"-" + str(quot) + ".xlsx"
    
    if refresh:
        try:
            os.remove(achievFilePath)
        except OSError:
            pass       

    achievFileHeader = ['代码','名称','每股收益','每股收益同比','每股净资产','净资产收益率(%)','每股现金流量(元)','净利润(万元)','净利润同比(%)','分配方案',
                       '发布日期']        
    if os.path.isfile(achievFilePath):
        achievDf = pd.read_excel(achievFilePath, index_col=False,encoding='utf-8')
        achievDf['代码'] = achievDf['代码'].astype('str')
        achievDf['代码'] = achievDf['代码'].apply(lambda x: x.zfill(6))        
    else:
        achievDf = ts.get_report_data(year,quot)
        print(achievDf.head(5))
#         achievDf.reset_index(level=0, inplace=True)
        achievDf['code'] = achievDf['code'].apply(lambda x: x.zfill(6))
        achievDf['code'] = achievDf['code'].astype('str')
        achievDf.to_excel(achievFilePath, header=list(achievFileHeader), encoding='utf-8', index = False)
        
    epcfCond = achievDf['每股现金流量(元)'] >= 0
    achievDfFilter = achievDf.loc[epcfCond]
    
    achievFilterFilePath = "..//achiev-filter-" + str(year) +"-" + str(quot) + ".xlsx"
    achievDfFilter.to_excel(achievFilterFilePath, header=list(achievDfFilter), encoding='utf-8', index = False)     
    
getHighValue(2018,2,0)  