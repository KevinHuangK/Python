#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬取51job的数据'
__author__ = 'intern'
__mtime__ = '2017/11/10'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
爬取的过程中有的会报错 也就是数据库中的数据会少几条或者十几条等等 那是因为可恶的51工程师投机取巧把丢失的数据对应的页面中的相应的<>标签
"""
import scrapy
from job.items import JobItem
from bs4 import BeautifulSoup
from sqlalchemy.sql.operators import div
import types


class JobSpider(scrapy.Spider):
	name = 'job'

	# 想要爬取不同类别的职位信息，在这里进行处理就可以(找规律 添加url就行)
	start_urls = [
		'http://search.51job.com/list/020000,000000,0000,00,9,99,Android,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
	]

	def parse(self,response):
		total_page = response.xpath('//*[@id="resultList"]/div[54]/div/div/div/span[1]/text()').extract_first()
		total_page = total_page[1:4]
		urls = []
		#如果想要爬取51job全部的Android数据 将10换成total_page + 1
		for i in range(1,10):
			urls.append('http://search.51job.com/list/020000,000000,0000,00,9,99,Android,2,{0}.html?lang=c&amp;stype=1&amp;postchannel=0000&amp;workyear=99&amp;cotype=99&amp;degreefrom=99&amp;jobterm=99&amp;companysize=99&amp;lonlat=0%2C0&amp;radius=-1&amp;ord_field=0&amp;confirmdate=9&amp;fromType=&amp;dibiaoid=0&amp;address=&amp;line=&amp;specialarea=00&amp;from=&amp;welfare='.format(i))
		for url in urls:
			yield scrapy.Request(url,callback=self.parse_data)


	def parse_data(self, response):
		a = 3
		#这里使用css选择器很方便
		for job1 in response.css('div.el'):

			a += 1
			url = job1.xpath('//*[@id="resultList"]/div['+str(a)+']/p/span/a/@href').extract_first()
			yield scrapy.Request(url, callback=self.parse_item)
			"""
			#存储为json数据
			yield {
				'type':"1",
				'ename':job1.xpath('//*[@id="resultList"]/div['+str(a)+']/span[1]/a/@title').extract_first(),
				'postinfo':job1.xpath('//*[@id="resultList"]/div['+str(a)+']/p/span/a/@title').extract_first(),
				'salary':job1.xpath('//*[@id="resultList"]/div['+str(a)+']/span[3]/text()').extract_first(),
				'oldurl':job1.xpath('//*[@id="resultList"]/div['+str(a)+']/p/span/a/@href').extract_first(),
				'releasetime':job1.xpath('//*[@id="resultList"]/div['+str(a)+']/span[4]/text()').extract_first()
			}
			"""

	def parse_item(self, response):
		item = JobItem()
		item['type'] = "1"
		item['ename'] = str(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title').extract()[0])
		item['postinfo'] = str(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a/@title').extract()[0])
		#这个字段对应的标签在有的Html 标签中也是不对的 只是需要点时间去查找一下作下处理就行了
		item['salary'] = str(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract()[0])
		item['oldurl'] = response.url
		#51job上有的详情页中没有学历限制，所以只有三个<span>标签 这样有时会造成角标越界错误
		#个别爬取的信息错误也是由于标签问题导致
		try:
			item['releasetime'] = str(
				response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div/span[4]/text()').extract()[0])
		except IndexError as e:
			item['releasetime'] = str(
				response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div/span[3]/text()').extract()[0])
		return item
