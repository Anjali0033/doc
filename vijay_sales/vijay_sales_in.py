from logging import disable
from bs4 import BeautifulSoup as bs
from requests import Session
from lxml import html
from time import strftime
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"

def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'multitronic'
    country = 'finland'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//h1[@id="ContentPlaceHolder1_h1ProductTitle"]//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="priceMRP"]//span//span//text()')[1]).strip()
    discounted_price = ''.join(tree.xpath('//div[@class="priceMRP"]//span//span//text()')[0]).strip()   


def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    for products in soup.find_all("div","col-lg-12 col-xs-12"):
        names = (products.find("h2","Dynamic-Bucket-ProductName"))
        discounted_price = products.find("div","Dynamic-Bucket-vsp").text
        reg_price = products.find("div","Dynamic-Bucket-mrp dvpricepdlft").text
        if products.find("a","nabprod"): product_href = products.find("a","nabprod").get("href")
        print(product_href) 



urls = ['https://www.vijaysales.com/laptop-and-printer/laptops/brand/buy-lenovo-laptops']
for url in urls:
    crawling_listpage(url)