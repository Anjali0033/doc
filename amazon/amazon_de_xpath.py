from bs4 import BeautifulSoup as bs
from requests import Session
from lxml import html
import pandas as pd
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"

product_list=[]
def crawl_list(url):
    r = s.get(url)
    print(r)
    tree = html.fromstring(r.text)
    for product in tree.xpath('//div[@class="a-section a-spacing-medium"]'):
	    product_name = ''.join(product.xpath('..//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]//text()'))
	    product_price1 = ''.join(product.xpath('..//span[@class="a-price-whole"]//text()'))
	    product_price2 = ''.join(product.xpath('..//span[@class="a-price a-text-price"]//span[@class="a-offscreen"]//text()'))
	    image_url = ''.join(product.xpath('..//img[@class="s-image"]//@src'))
	    print(product.xpath('..//img[@class="s-image"]//@src'))
	    product_href = ''.join(product.xpath('..//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]//a[@class="a-link-normal a-text-normal"]//@href'))
	    # product_list.append({"product_name":product_name,"price1":product_price1,"price2":product_price2,"image_url":image_url,"product_href":product_href})


    if tree.xpath('//span[@class="celwidget slot=MAIN template=PAGINATION widgetId=pagination-button"]//li[@class="a-last"]'):
        url_page = ''.join(tree.xpath('//span[@class="celwidget slot=MAIN template=PAGINATION widgetId=pagination-button"]//li[@class="a-last"]//@href'))
        print(tree.xpath('//span[@class="celwidget slot=MAIN template=PAGINATION widgetId=pagination-button"]//li[@class="a-last"]//@href'))
        crawl_list("https://www.amazon.de"+url_page)


urls = ["https://www.amazon.de/s?i=computers&bbn=427957031&rh=n%3A427957031%2Cp_89%3ALenovo%2Cp_n_feature_fourteen_browse-bin%3A8321930031%7C8321931031%2Cp_n_condition-type%3A776949031&dc&qid=1629094899&rnid=776942031&ref=sr_pg_1"]
for url in urls:
    crawl_list(url)

# dict1 = pd.DataFrame(product_list)
# dict1.to_excel("amazon_de_listpage.xlsx",index=False)    