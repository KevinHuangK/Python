#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Boss直聘Spider'
__author__ = 'intern'
__mtime__ = '2017/11/20'
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
"""
import scrapy
import json
from bs4 import BeautifulSoup

from bossspider.items import BossspiderItem


class BossSpider(scrapy.Spider):
	#这是测试代理ip池 下面注释的代码是能爬取数据的代码
	"""
	def __init__(self):
	self.headers = {
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept-Encoding': 'gzip, deflate',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	}

	name = "proxie"
	allowed_domains = ["www.zhipin.com"]
	start_urls = ['http://www.zhipin.com/job_detail/?query=Java&scity=100010000&source=2']

	def parse(self, response):
		print(response.body)
	"""

	name = 'boss'

	allowed_domains = ["www.zhipin.com"]
	def start_requests(self):
		urls = [
			'http://www.zhipin.com/job_detail/?query=Java&scity=100010000&source=2',
		]
		for url in urls:
			yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		urls = []
		base_url = 'http://www.zhipin.com'
		jobs = response.xpath('//div[@class="job-primary"]')
		for index,job in enumerate(jobs):
			href = job.xpath('//*[@id="main"]/div[3]/div[2]/ul/li['+ str(int(index) + 1) +']/div[1]/div[1]/h3/a/@href').extract()
			print(href)
			if href is not None:
				url = base_url + href[0]
				urls.append(url)
		for url in urls:
			yield scrapy.Request(url, callback=self.parse_data)

		next_href = response.xpath('//div[@class="page"]/a/@href').extract()[-1]
		if next_href != 'javascript:;':
			next_page_url = 'http://www.zhipin.com/' + next_href
			yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)



	def parse_data(self,response):
		item = BossspiderItem()
		type = '3'
		ename = response.xpath('//*[@id="main"]/div[1]/div/div/div[3]/h3/a/text()').extract_first()
		postinfo = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/text()').extract_first()
		salary = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()').extract_first()
		oldurl = response.url
		releasetime = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[1]/span/text()').extract_first()
		item['type'] = type
		item['ename'] = ename
		item['postinfo'] = str(postinfo)
		# 这个字段对应的标签在有的Html 标签中也是不对的 只是需要点时间去查找一下作下处理就行了
		item['salary'] = str(salary)
		item['oldurl'] = str(oldurl)
		item['releasetime'] = releasetime
		return item





