# -*- coding: utf-8 -*-
# envir：pymongo, MongoDB, scrapy， python3
# atuhor:yabin

import random
import os
from datetime import datetime

import pymongo
import xlwt
import xlrd
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

import matplotlib.pyplot as plt


def run_scrapy(spider):
    """
    利用scrapy爬虫框架启动weahter爬虫抓取从2011-2019年所有月份的天气数据信息，并存放到MangoDB数据库中
    """
    project_settings = get_project_settings()
    process = CrawlerProcess(project_settings)
    process.crawl(spider)
    process.start()
    process.join()  # 进程间同步
    
def read_weather_info():
    """
    判断数据库中是否存储数据
        if 未存储:直接启动爬虫
        else：直接随机连接集合，读取数据
    """
    client = pymongo.MongoClient(host='localhost')
    db = client["weather_info"]
    colls_name = coll_names = db.list_collection_names(session=None)
    if len(colls_name) == 0:
        # 启动爬虫，爬取并存放数据
        run_scrapy('weather')

    colls_name = coll_names = db.list_collection_names(session=None)  # 重新获取
    random_colls = random.choice(colls_name)
    print(random_colls+':')
    collection = db[random_colls]
    
    return collection
    
def data_handle(collection, flag=""):
    """提取想要的数据信息"""
    highs = []
    lows = []
    dates = []
    for coll in collection:
        highs.append(coll['h_temp'])
        lows.append(coll['l_temp'])
        dates.append(coll['date'])
        
    av_high = round(sum(highs) / len(highs), 1) # 保留一位有效数字
    av_low = round(sum(lows) / len(lows), 1)
    
    if flag=="":
        print('当月每天最高温度：', highs)
        print('当月平均最高温度:', av_high)
        print('当月每天最低温度:', lows)
        print('当月平均最低温度:', av_low)
        print('当月最高温度:', max(highs))
        print('当月最低温度:', min(lows))
        return collection.collection.name, max(highs), min(lows), av_high, av_low, 
    else :
        return dates, highs, lows
    
def set_style(color_index=0, bold=False):
    """excel格式"""
    style = xlwt.XFStyle()
    #创建对其实例
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    
    #创建字体实例
    font_mine = xlwt.Font()
    font_mine.name = '微软雅黑'
    font_mine.bold = bold
    font_mine.colour_index = color_index
    
    #关联style
    style.font = font_mine
    style.alignment = alignment
    return style
    
def write_to_xls(month_data, row_num=0):
    """写入表格中"""
    #单元格样式
    COLOR_BLUE = 4
    COLOR_RED = 2
    
    if row_num == 0:
        row0 = ['月份', '最高温度', '最低温度', '月平均最高温度', '月平均最高温度']
        data = [row0, month_data]
    else:
        data = [month_data]
        
    # 重新写入表格
    f = xlwt.Workbook()
    sheet = f.add_sheet('sheet', cell_overwrite_ok=True)

    for i in range(row_num, len(data)):
        row_data = data[i]
        for j in range(len(row_data)):
            # flag = i
            cell_data = data[i][j]
            style = set_style()
            #第一行加粗
            if i == 0:
                style = set_style(bold=True)
            # 最高标红，最低标蓝
            if i != 0 and j == 1:
                style = set_style(COLOR_RED, True)
            elif i != 0 and j == 2:
                style = set_style(COLOR_BLUE, True)
            #if row_num != 0:
            #   i = row_num +1
            sheet.write(i, j, cell_data, style)
            #i = flag
        
    f.save('单月天气情况.xls')
    
    
def draw_line(dates, highs, lows):
    """根据数据绘制图形"""
    # new_dates = []
    # for date in dates:
    #    new_date = datetime.strptime(date, "%Y-%m-%d")
    #    new_dates.append(new_date)
    fig = plt.figure(dpi=128, figsize=(16, 5))
    plt.plot(dates, highs, c='red')
    plt.plot(dates, lows, c='blue')

    #设置图形格式
    plt.title("Daily high and lows temperatures", fontsize=24)
    plt.xlabel('',fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel("Temperature (℃)",fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=14)
    
    plt.show()
    
if __name__=='__main__':
    
    collection = read_weather_info()
    # 提取数据
    month_data = data_handle(collection.find())
    
    #如果文件不存在直接写入数据，如果存在从已有文档后插入数据
    if os.path.exists("单月天气情况.xls"):
        write_to_xls(list(month_data)[:-1])
    else:
        #workbook = xlrd.open_workbook(r'.\单月天气情况.xls', 
        #    encoding_override='gb2312')
        #table = workbook.sheet_by_name('sheet')
        #write_to_xls(list(month_data), table.nrows)
        write_to_xls(list(month_data)[:-1])
        
    # 绘制图形
    month_data = data_handle(collection.find(), flag="draw")
    draw_line(month_data[0], month_data[1],  month_data[2])