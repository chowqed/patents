import scrapy
from patents.items import PatentsItem
from collections import OrderedDict

def url_list():
	list=[]
	year=range(1976,1978)
	month1=['1','4','7','10']
	month2=['3','6','9','12']
	day1=['1','1','1','1']
	day2=['31','30','30','31']
	c1='%2F'
	c2='-%3E'
	c3='&d=PTXT'
	str1='http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=IC%2F%28Toronto+OR+Ottawa+OR+Mississauga+OR+Hamilton+OR+Brampton+OR+London+OR+Markham+OR+Vaughan+OR+Windsor+OR+Kitchener+OR+Burlington+OR+Sudbury+OR+Oshawa+OR+%22St+Catherines%22+OR+Barrie+OR+Cambridge+OR+Kingston+OR+Guelph+OR+%22Thunder+Bay%22+OR+Waterloo+OR+Woodstock+OR+Kanata%29+AND+ICN%2FCA+AND+ISD%2F'
	str2='http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=IC%2F%28Montreal+OR+Quebec+OR+Gatineau+OR+Sherbrooke+OR+Trois-Rivieres+OR+Chicoutimi+OR+Richelieu+OR+Chaeauguay+OR+Drummonville+OR+Saint-Jerome+OR+Saint-Hyacinthe%29+AND+ICN%2FCA+AND+ISD%2F'
	for j in range(1996,2011):
		for i in range(4):
			url=str2+month1[i]+c1+day1[i]+c1+str(j)+c2+month2[i]+c1+day2[i]+c1+str(j)+c3
			list.append(url)

	return list


class patentspider(scrapy.Spider):
	name = 'patent'
	allowed_domains = ["patft.uspto.gov"]
	start_urls = url_list() 
	CONCURRENT_REQUESTS_PER_DOMAIN=1
	DOWNLOAD_DELAY = 1 
	def parse(self, response):
		item = PatentsItem()
		date = response.selector.xpath("//span[@id]/text()").re(r'[0-9]+')
		num = response.selector.xpath("//body/text()").re(r'[0-9]+')
		item['sdate'] = date[0]
		item['edate'] = date[1]
		item['patents'] = num
		yield item
