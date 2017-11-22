#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬取拉勾网数据'
__author__ = 'intern'
__mtime__ = '2017/11/17'
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
爬取拉勾网的数据有些恶心：
    1.伪装的ajax请求，而且是post请求 如果爬虫的url直接使用浏览器上的地址那么返回的招聘信息是空的 需要使用F12下的NetWork-->XHR
    2.Ajax请求返回的数据时json串 只需要将json转换为对象就行
    3.下一页对应的Ajax请求的url是有规律的，说白了就是post请求携带的数据有一个字段pn是有规律的
    4.返回的json串中直接能计算出招聘的数据一共有多少页

拉勾网访问太过于频繁的话会返回{'success': False, 'msg': '您操作太频繁,请稍后再访问', 'clientIp': '211.160.167.138'}
"""
import scrapy
import json,math,re,types,logging

from lagouspider.items import LagouspiderItem
from scrapy import FormRequest


class LaGouSpider(scrapy.Spider):
	name = 'lagou'

	allowed_domains = ["lagou.com"]
	base_url = 'https://www.lagou.com/jobs/positionAjax.json'
	cookie = "user_trace_token=20170710081952-7e5f16c8-6505-11e7-a6de-5254005c3644; LGUID=20170710081952-7e5f1ed8-6505-11e7-a6de-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAACDBAAIA841799FBB1D9FFF00CB94A785E3D7BBB; _gat=1; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUsj9AKNp00000PW4pNb00000YlaMBM.THL0oUhY1x60UWdBmy-bIy9EUyNxTAT0T1dBmhfzn1nYnj0snj79m1b10ZRqrRwKfHIKfWfkPW7KfbcswRFKPj9jnbN7wH6Yn16dwHT0mHdL5iuVmv-b5Hnsn1nznjR1njfhTZFEuA-b5HDv0ARqpZwYTZnlQzqLILT8UA7MULR8mvqVQ1qdIAdxTvqdThP-5ydxmvuxmLKYgvF9pywdgLKW0APzm1YznWc3P0%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117464%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D220%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26issp%3D1%26f%3D3%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26inputT%3D2723%26prefixsug%3D%2525E6%25258B%252589%2525E9%252592%2525A9%26rsp%3D0; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; X_HTTP_TOKEN=5b487a0ad0599a0e9c44a0c7eacd912f; TG-TRACK-CODE=index_search; _gid=GA1.2.1801735249.1511332153; _ga=GA1.2.925518107.1499646020; LGSID=20171122142749-42fc4d3b-cf4e-11e7-9986-5254005c3644; LGRID=20171122143057-b2e5948c-cf4e-11e7-9d0d-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510905337,1510905356,1511332154,1511332226; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1511332341; SEARCH_ID=5fa69f3c855d411fb615a14f9c18937a"
	"""
	header = {
		'Accept': 'application / json, text / javascript, * / *; q = 0.01',
		'Accept-Encoding':'gzip,deflate,br',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'Content-Length':'24',
		'Cookie':cookie,
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Host':'www.lagou.com',
		'Origin':'https://www.lagou.com',
		'Referer':'https://www.lagou.com/jobs/list_Java?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
		'User-Agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36',
		'X-Anit-Forge-Code':'0',
		'X-Anit-Forge-Token':'None',
		'X-Requested-With':'XMLHttpRequest',
	}
	"""
	headers = {
		'Cookie': cookie,
		'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36',
		'Referer': 'https://www.lagou.com/jobs/list_Java?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
	}
	# 'px': 'default',
	base_data = {
		'city': '北京',
		'needAddtionalResult': 'false',
		'isSchoolJob': '0',
		'kd': 'Java',
		'first': 'true',
		'pn': '1'
	}
	# form_data = {
	# 	'kd': 'Java',
	# 	'first': 'true',
	# 	'pn': '1'
	# }
	def start_requests(self):
		url = self.parse_url(self.base_url, self.base_data)
		print("=========%s" % url)
		yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)
		# return [FormRequest(url=url,headers=self.headers,formdata=self.form_data,callback=self.parse)]
	def parse_url(self, url, data):
		params = []
		for key in data:
			params.append(key + '=' + str(data[key]))
		return url + '?' + '&'.join(params)

	def parse(self,response):
		print('-' * 50)
		print(response.url)
		# print(type(str(response._body)))
		data = json.loads(response._body,encoding='utf-8')
		max_pages = int(math.ceil(data['content']['positionResult']['totalCount'] / float(data['content']['pageSize'])))

		"""
			改变post请求的携带参数，这里请求了所有页的数据
			对于拉勾网的真实数据都是隐藏在ajax请求返回的json串中的，
			本应该是post请求，这里需要将post请求携带的参数拼接成get请求
		"""
		# urls = []
		# max_page = max_pages + 1
		# for i in range(1, max_page):
		# 	self.form_data['pn'] = str(i)
		# 	datas.append(self.form_data)
		# for data in datas:
		# 	print(data)
		# 	return [FormRequest(url=self.parse_url(self.base_url, self.base_data), headers=self.headers, formdata=data, callback=self.parse_data)]

		urls = []
		max_page = max_pages + 1
		for i in range(1, max_page):
			print(i)
			self.base_data['pn'] = i
			urls.append(self.parse_url(self.base_url, self.base_data))
		for url in urls:
			yield scrapy.Request(url=url, headers=self.headers,
								callback=self.parse_data,dont_filter=True)

	def parse_data(self,response):
		try:
			base_url = 'https://www.lagou.com/jobs/{0}.html'
			res = json.loads(response._body)
			results = res['content']['positionResult']['result']
			items = []
			for rt in results:
				item = LagouspiderItem()
				item['type'] = "4"
				item['ename'] = rt['companyShortName']  # 公司简称
				item['postinfo'] = rt['positionName']  # 招聘的职位
				item['salary'] = rt['salary']  # 薪资
				posId = str(rt['positionId'])
				item['oldurl'] = base_url.format(posId)  # 详情url
				item['releasetime'] = rt['createTime']  # 创建时间
				yield item
		except Exception as e:
			self.log('访问太过于频繁',level=logging.ERROR)


