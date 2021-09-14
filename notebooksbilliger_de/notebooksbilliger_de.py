import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import Session
from lxml import html
from googletrans import Translator
from time import strftime
translator = Translator()
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

def detail_page(product_href):
    r = s.get(product_href)
    tree = html.fromstring(r.text)
    retailer = 'notebooksbilliger'
    country = 'germany'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//h1[@class="name squeezed"]//text()')).strip()
    reg_price = ''.join(tree.xpath('//div[@class="product-price__uvp-wrapper"]//span[@class="product-price__uvp dp-inbl va-mid"]//text()')).strip()
    discounted_price = ''.join(tree.xpath('//div[@class="product-price__container "]//div[@class="product-price__wrapper"]//span[@class="product-price__regular js-product-price"]//text()')).strip()
    part_no = ''.join(tree.xpath('//table[@class="properties_table"]//tr//td[@class="group_header_wrapper produktDetails_eigenschaft1"][contains(string(),"Herstellernummer:")]//ancestor::tr//td[@class="group_header_wrapper"]//text()')).strip()
    model_no = ''.join(tree.xpath('//table[@class="properties_table"]//tr//td[@class="group_header_wrapper produktDetails_eigenschaft1"][contains(string(),"EAN-Nummer")]//ancestor::tr//td[@class="group_header_wrapper"]//text()')).strip()
    stock = translator.translate(''.join(tree.xpath('//div[@class="deal_duration"]//strong//text()'))).text


    try:
        table = "create table coolblue_be(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into notebooksbilliger_de(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into notebooksbilliger_de(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()


    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")

def crawl_list(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    for product in tree.xpath('//div[@class="js-ado-product-click  mouseover  clearfix js-listing-item-GTM js-event-collector-product"]'):

        product_href = product.xpath('..//div[@class="product_name"]//a[@class="listing_product_title"]//@href')
        for ref in product_href:            
            detail_page(str(ref))


    if tree.xpath('//a[@class="dp-inbl va-mid nbb-pagination-page"]//span[contains(string(),"nächste Seite")]//ancestor::a//@href'):
        print(tree.xpath('//a[@class="dp-inbl va-mid nbb-pagination-page"]//span[contains(string(),"nächste Seite")]//ancestor::a//@href'))
        url_page = tree.xpath('//a[@class="dp-inbl va-mid nbb-pagination-page"]//span[contains(string(),"nächste Seite")]//ancestor::a//@href')
        crawl_list("https://www.notebooksbilliger.de"+ url_page[1])
    
urls = ["https://www.notebooksbilliger.de/notebooks/lenovo+notebooks"]
for url in urls:
    crawl_list(url)    
