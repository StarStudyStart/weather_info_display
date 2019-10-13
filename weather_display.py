# -*- coding: utf-8 -*-
# envir：pymongo, MongoDB, scrapy
# atuhor:yabin

import random

import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


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
    
def data_handle(collection):
    """提取想要的数据信息"""
    high = []
    low = []
    for coll in collection:
        high.append(coll['h_temp'])
        low.append(coll['l_temp'])
        
    av_high = round(sum(high) / len(high), 1) # 保留一位有效数字
    av_low = round(sum(low) / len(low), 1)
    
    print('当月每天最高温度：', high)
    print('当月平均最高温度:', av_high)
    print('当月每天最低温度:', low)
    print('当月平均最低温度:', av_low)
    print('当月最高温度:', max(high))
    print('当月最低温度:', min(low))
    
    return av_high, av_low, max(high), min(low)
    
if __name__=='__main__':
    
    collection = read_weather_info()
    # 提取数据
    av_high, av_low, high, low = data_handle(collection.find())
