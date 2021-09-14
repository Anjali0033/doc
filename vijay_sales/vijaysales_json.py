from requests import Session
import json
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from lxml import html
import time
import json
all_items = []

s = Session()
str_time = time.strftime("%Y-%m-%d")
head = {"Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"en-US,en;q=0.5",
"Connection":"keep-alive",
"Content-Length":"443",
"Content-Type":"application/json; charset=utf-8",
"Cookie":"ASP.NET_SessionId=pmo1fejxdjzpwdkcieqpe3ck; __AntiXsrfToken=70d53903c1a9467cba751dde98cf4597; _gcl_au=1.1.677410506.1627626608; mycity=cityId=1&city=Mumbai&IsPreOrder=false; Mypreurl=; _ga=GA1.2.217501665.1627626609; _gid=GA1.2.11269500.1627626609; _fbp=fb.1.1627626609480.2109145657; _clck=1jk33ht; _clsk=1khcils|1627637584484|9|1|eus2-b/collect; ViewedProductCookie=RVP=16005,14493,16022,; flixgvid=flixb56d4c1a000000.88923192; inptime0_9295_in=0; _uetsid=95d38e70f0ff11eb8c4a0ff6922f60da; _uetvid=95d3ba30f0ff11ebbf8491a2f74555e3".encode("utf-8"),
"Host":"www.vijaysales.com",
"Origin":"https://www.vijaysales.com",
"Referer":"https://www.vijaysales.com/laptop-and-printer/computers/buy-laptops-laptop-and-printer?COMPUTERS=Laptops,Desktops&PRICE=21990to279999",
"Sec-Fetch-Dest":"empty",
"Sec-Fetch-Mode":"cors",
"Sec-Fetch-Site":"same-origin",
"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
"X-Requested-With":"XMLHttpRequest"}
s.headers.update(head)

def crawl_details(url):
	global str_time
	s = Session()
	s.headers["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
	s_response = s.get(url)
	s_tree = html.fromstring(s_response.text)
	version = ''.join(s_tree.xpath("//input[@id='ContentPlaceHolder1_hfVersion']//@value")).strip()
	city_id = ''.join(s_tree.xpath("//input[@id='ContentPlaceHolder1_hfCityID']//@value")).strip()
	prd_id = url.split("/")[-1]
	data = {'ProductID':'{}'.format(prd_id),'CityID':'{}'.format(city_id),'Version':'{}'.format(version)}
	head = {"Accept":"application/json, text/javascript, */*; q=0.01",
			"Accept-Encoding":"gzip, deflate, br",
			"Accept-Language":"en-US,en;q=0.5",
			"Connection":"keep-alive",
			"Content-Length":"49",
			"Content-Type":"application/json;charset=utf-8",
			"Cookie":"_nv_uid=38961852.1630399925.d5e45e01-b84c-4560-a36c-0ac2706b749f.1630680185.1630731653.6; _nv_utm=38961852.1630399925.6.1.dXRtc3JjPShkaXJlY3QpfHV0bWNjbj0oZGlyZWN0KXx1dG1jbWQ9KG5vbmUpfHV0bWN0cj0obm90IHNldCl8dXRtY2N0PShub3Qgc2V0KXxnY2xpZD0obm90IHNldCk=; _nv_did=38961852.1630399925.20319223668hr6tr; _nv_hit=38961852.1630731667.cHZpZXc9Mg==; _fbp=fb.1.1630399930005.1196209240; _clck=xrn0vp|1|eug|0; nv_push_times=3; _clsk=noll8x|1630731670220|2|1|b.clarity.ms/collect; ASP.NET_SessionId=lhvb40a5sq2iivts0hwbavob; __AntiXsrfToken=d7e2e31019cb4f68944d7f1af7847b45; _nv_pv=2; _nv_sess=38961852.1630731653.IunA7eUUOG2BNwvxPSfaVkDWU5fHB7dOZQno3BMG4ox4y3WFNT; mycity=cityId=1&city=Mumbai&IsPreOrder=false; Mypreurl=; nv_push_neg=1".encode("utf-8"),
			"Host":"www.vijaysales.com",
			"Origin":"https://www.vijaysales.com",
			"Referer":"https://www.vijaysales.com/apple-myd82hn-a-macbook-pro-apple-m1-chip-8gb-ram-256-gb-ssd-13-3-33-78-cm-display-integrated-graphics-mac-os-big-sur-space-grey/15041".encode("utf-8"),
			"Sec-Fetch-Dest":"empty",
			"Sec-Fetch-Mode":"cors",
			"Sec-Fetch-Site":"same-origin",
			"TE":"trailers",
			"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
			"X-Requested-With":"XMLHttpRequest"}
	s = Session()
	# print(s_response.url)
	s.headers.update(head)
	api_url = "https://www.vijaysales.com/ProductPageNew.aspx/loadSpecification"
	r = s.post(api_url,json.dumps(data))
	js = r.json()["d"]
	print("=----------{}".format(r.url))
	# print("Response -> {}".format())
	soup = bs(s_response.content,"html.parser")
	tree = html.fromstring(js)
	# print("-----------> {}".format(js))
	processor_details = ""
	name = soup.find("h1").text
	sales_price = soup.find("div","priceMRP").find("span","to_top").next.next.next.text
	mrp_price = soup.find("div","priceMRP").find("span","unstikeprize")
	if mrp_price:
		mrp_price = mrp_price.text
	else:
		mrp_price ="Not given"

	brand = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"BRAND")]//following-sibling::div//text()'))).strip()
	model_name = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"MODEL NAME")]//following-sibling::div//text()'))).strip()
	series = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"SERIES")]//following-sibling::div//text()'))).strip()
	sku = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"SKU")]//following-sibling::div//text()'))).strip()
	os = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"OS")]//following-sibling::div//text()'))).strip().replace("  ","")
	processor_brand = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"PROCESSOR BRAND")]//following-sibling::div//text()'))).strip().replace("  ","")
	processor = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"PROCESSOR")]//following-sibling::div//text()'))).strip().replace("  ","")
	processor_varient = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"VARIENT")]//following-sibling::div//text()'))).strip().replace("  ","")
	screen_size = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"SCREEN SIZE")]//following-sibling::div//text()'))).strip().replace("  ","")
	resolution = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"RESOLUTION")]//following-sibling::div//text()'))).strip().replace("  ","")
	ram =  ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"RAM")]//following-sibling::div//text()'))).strip().replace("  ","")
	hdd_type = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"HDD CAPACITY")]//following-sibling::div//text()'))).strip().replace("  ","")
	ssd_type = ''.join(set(tree.xpath('//div[@class="cls-ty sptyp" and contains(string(),"SSD CAPACITY")]//following-sibling::div//text()'))).strip().replace("  ","")	
	type_graphics = ''.join(tree.xpath("//li[@class='sphdT spHed' and contains(string(),'GRAPHICS')]//following-sibling::li//div[contains(string(),'TYPE')]//div[@class='cls-vl spval']//text()")[0]).strip()
	graphics = ''.join(tree.xpath("//li[@class='sphdT spHed' and contains(string(),'GRAPHICS')]//following-sibling::li//div[contains(string(),'PROCESSOR')]//div[@class='cls-vl spval']//text()")).strip()
	graphics_capacity = ''.join(tree.xpath("//li[@class='sphdT spHed' and contains(string(),'GRAPHICS')]//following-sibling::li//div[contains(string(),'CAPACITY')]//div[@class='cls-vl spval']//text()")).strip()
	graphics = type_graphics+"|"+graphics+"|"+graphics_capacity
	
	ctg = "Laptops"
	try:	
		for cat in soup.find("ul",id="ContentPlaceHolder1_ULSideMap").find_all("li"):
			if cat.text.lower() == "desktops":
				ctg = "Desktop"
			
			elif cat.text.lower() == "laptops":
				ctg = "Laptops"
	except:
		pass           


	data = {
		"Category":ctg,
		"URL":s_response.url,
		"Product name":name,
		"Sales price":sales_price,
		"MRP price":mrp_price,
		"Brand":brand,
		"Model_Name":model_name,
		"Series":series,
		"SKU":sku,
		"Operating System":os,
		"Processor Brand":processor_brand,
		"Varient":processor_varient,
		# "Chipset":processor_chipset,
		"Processor":processor_details,
		"Screen Size":screen_size,
		"Resolution":resolution,
		"RAM":ram,
		"HDD Type":hdd_type,
		"SSD Type":ssd_type,
		"Graphics":graphics,
		"Date":str_time
	}
	print(data)
	all_items.append(data)

url = "https://www.vijaysales.com/searchpage.aspx/_getRHSProducts"
next = 1
for index in range(60,97,12):
	prev = index
	data = {"CategoryID":"4",
			"CityId":1,
			"FilterValueIDs":"510,:511,:",
			"FilterId":"54",
			"Keywords":"",
			"MinAmount":"21990.00",
			"MaxAmount":"279999.00",
			"SortBy":0,
			"StartIndex":next,
			"EndIndex":prev,
			"OfferType":0,
			"InStockOnly":0,
			"prdFilterVal":"",
			"FlagPrice":"",
			"fvalid":"510",
			"CategoryName":"",
			"FilterName":"",
			"FilterValueName":"",
			"isScroll":"true",
			"MainFilterName":"",
			"PrimaryFilterID":"510",
			"BucketProductIDs":"",
			"opertion":":TYPE@54:510,:@54:511,:",
			"BrandID":"0"}
	
	next = prev+1
	r = s.post(url,data=json.dumps(data))
	js = r.json()
	# print(js['d'])
	soup = bs(js["d"],"html.parser")
	for products in soup.find_all("ul","Xbxslider Xinner-slider padding-top15"):
		product_href = products.find("a").get("href")
		print(product_href)
		crawl_details(product_href)


df = pd.DataFrame(all_items)
df.to_excel("vijay_sales{}.xlsx".format(str_time),index=False)