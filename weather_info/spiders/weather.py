# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from weather_info.items import WeatherInfoItem

class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['lishi.tianqi.com']
    start_urls = ['http://lishi.tianqi.com/hangzhou/index.html']

    def parse(self, response):
        href_weahers = response.css('.tqtongji1 a::attr(href)').extract()
        for href in href_weahers:
            yield Request(href, callback=self.parse_weather_info)
            
    
    def parse_weather_info(self, response):
        month_weather = response.css('#tool_site .box-hd .box-t-l::text').extract()[1]
        weather_info = response.css('.tqtongji2 ul')[1:]  # 删除第一行标题数据
        for day_weather in weather_info:
            item = WeatherInfoItem()
            item['collection'] = month_weather
            info = day_weather.css('li ::text').extract() # ::text前加空格提取自身及子标签内容，部分天气接口含有链接，仅提取li标签内容会出错
            #info1 = day_weather.xpath('. //li//text()').extract()
            #print(day_weather.extract())
            #print(info1)
            # print(info)
            item['date'] = info[0]
            item['h_temp'] = int(info[1])
            item['l_temp'] = int(info[2])
            item['info'] = info[3]
            item['w_dir'] = info[4]
            item['w_level'] = info[5]
            yield item
            
            
        #print(weather_info)
