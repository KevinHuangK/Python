#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬取智联的数据'
__author__ = 'intern'
__mtime__ = '2017/11/21'
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
from bs4 import BeautifulSoup

from zhilianspider.items import ZhilianspiderItem


class ZhiLianSpider(scrapy.Spider):
	name = 'zhilian'

	allowed_domains = ["zhaopin.com"]
	base_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx'
	base_data = {
		'jl': '北京',
		'kw': 'Java',
		'sm': '0',
		'sg': '178038a789504e8ab6b82ef03790545e',
		'p':'1',
	}

	def start_requests(self):
		url = self.parse_url(self.base_url, self.base_data)
		yield scrapy.Request(url=url, callback=self.parse)

	def parse_url(self, url, data):
		params = []
		for key in data:
			params.append(key + '=' + str(data[key]))
		return url + '?' + '&'.join(params)

	def parse(self, response):
		print('-' * 50)
		print(response.url)
		soup = BeautifulSoup(response._body, 'lxml')
		datas = soup.find_all('table', {'class': 'newlist'})
		#这是遍历当前页的所有条目的详情页
		detail_urls = []
		for index in range(1,len(datas)):
			url = datas[index].find('td',{'class': 'zwmc'}).find('div').find('a').get('href')
			detail_urls.append(url)
		for url in detail_urls:
			yield scrapy.Request(url=url,callback=self.parse_data)

		#获取之后的8页数据 2-9页
		next_urls = []
		for i in range(2, 10):
			self.base_data['p'] = i
			next_urls.append(self.parse_url(self.base_url, self.base_data))
		for url in next_urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse_data(self,response):
		soup = BeautifulSoup(response._body, 'lxml')
		item = ZhilianspiderItem()
		item['type'] = "5"
		item['ename'] = str(soup.find('a',{'target': '_blank'}).get_text())
		item['postinfo'] = str(soup.find('div',{'class': 'inner-left fl'}).find('h1').get_text().replace(" ","").replace("\r\n"," ").replace("\n",""))
		item['salary'] = str(soup.find('ul',{'class': 'terminal-ul clearfix'}).find_all('li')[0].find('strong').get_text())
		item['oldurl'] = response.url
		item['releasetime'] = str(soup.find('ul',{'class': 'terminal-ul clearfix'}).find_all('li')[2].find('strong').find('span').get_text())
		return item

