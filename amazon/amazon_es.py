from bs4 import BeautifulSoup as bs
from requests import Session
from lxml import html 
from time import strftime
import sys
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0" 
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()
table_listpage= "create table amazon_es_listpage(SKU_id varchar(100) null,extraction_date varchar(200) null,product_name varchar(500) null,reg_price varchar(500) null,list_price varchar(500) null,product_rating varchar(500) null,product_href varchar(500) null);"
table_detailpage= "create table amazon_es_detailpage(SKU_id varchar(100) null,extraction_date varchar(200) null,product_processor varchar(500) null,product_modelno varchar(500) COLLATE utf8_unicode_ci,product_RAM varchar(500) null,product_HDD varchar(500) null);"
cur.execute(table_listpage)
cur.execute(table_detailpage)
con.commit()

def detail_page(product_href):
    r = s.get(product_href)
    tree = html.fromstring(r.text)
    print(r)
    SKU_id = (''.join(tree.xpath('//div[@class="a-section"]//tr//th[@class="a-color-secondary a-size-base prodDetSectionEntry"][contains(string(),"ASIN")]//ancestor::tr//td[@class="a-size-base prodDetAttrValue"]//text()')))
    extraction_date = strftime("%A, %d %b %Y ,%r")
    product_processor = (''.join(tree.xpath('//div[@class="a-expander-content a-expander-extend-content"]//tr//th[@class="a-color-secondary a-size-base prodDetSectionEntry"][contains(string(),"Fabricante del procesador")]//ancestor::tr//td[@class="a-size-base prodDetAttrValue"]//text()')))
    product_modelno = (''.join(tree.xpath('//div[@class="a-expander-content a-expander-extend-content"]//tr//th[@class="a-color-secondary a-size-base prodDetSectionEntry"][contains(string(),"Número de modelo del producto") or contains(string(),"Referencia del fabricante")]//ancestor::tr//td[@class="a-size-base prodDetAttrValue"]//text()')))
    product_RAM = (''.join(tree.xpath('//div[@class="a-expander-content a-expander-extend-content"]//tr//th[@class="a-color-secondary a-size-base prodDetSectionEntry"][contains(string(),"Capacidad de la memoria RAM")]//ancestor::tr//td[@class="a-size-base prodDetAttrValue"]//text()')))
    product_HDD = (''.join(tree.xpath('//div[@class="a-expander-content a-expander-extend-content"]//tr//th[@class="a-color-secondary a-size-base prodDetSectionEntry"][contains(string(),"Descripción del disco duro")]//ancestor::tr//td[@class="a-size-base prodDetAttrValue"]//text()')))

    query = "SELECT * FROM amazon_es WHERE SKU_id='{}' and extraction_date='{}' fetch(SKU_id,extraction_date)"
    cur.execute(query)
    if(not cur.fetchone()):
        insert_query = "insert into amazon_es_detail_page(SKU_id,extraction_date,product_processor,product_modelno,product_RAM,product_HDD) VALUES (%s,%s,%s,%s,%s,%s);"
        VALUES = (SKU_id,extraction_date,product_processor,product_modelno,product_RAM,product_HDD)
        cur.execute(insert_query,VALUES)
        con.commit()    


def crawling_list(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    print('okay')
    for products in soup.find_all("div","sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"):
        SKU_id = products.find("a","a-link-normal a-text-normal").get("href").split('/')[3]
        extraction_date = strftime("%A, %d %b %Y ,%r")
        product_name = products.find("span","a-size-base-plus a-color-base a-text-normal").text
        if products.find("span","a-price-whole"): reg_price = products.find("span","a-price-whole").text
        else: reg_price = '' 
        if products.find("span","a-price a-text-price"): list_price = products.find("span","a-price a-text-price").find("span","a-offscreen").text.replace(" €","")
        else: list_price = ''
        if products.find("span","a-size-base"): product_rating = products.find("span","a-size-base").text
        else: product_rating = ''
        product_href = products.find("a","a-link-normal a-text-normal").get("href")
        detail_page("https://www.amazon.es"+product_href)

        query = "SELECT * FROM amazon_es WHERE SKU_id='{}' and extraction_date='{}' fetch(SKU_id,extraction_date)"
        cur.execute(query)
        if(not cur.fetchone()):
            insert_query = "insert into amazon_es_listpage(SKU_id,extraction_date,product_name,reg_price,list_price,product_rating,product_href) VALUES (%s,%s,%s,%s,%s,%s,%s);"
            VALUES = (SKU_id,extraction_date,product_name,reg_price,list_price,product_rating,product_href)
            cur.execute(insert_query,VALUES)
            con.commit() 

    soup.find("ul","a-pagination")
    if soup.find("ul","a-pagination").find("li","a-last"):
        print(soup.find("ul","a-pagination").find("li","a-last").find("a").get("href"))
        url_page = soup.find("ul","a-pagination").find("li","a-last").find("a").get("href")
        crawling_list("https://www.amazon.es"+url_page)
    else:
        sys.exit()

urls = ['https://www.amazon.es/s?i=computers&bbn=938008031&rh=n%3A938008031%2Cp_89%3ALenovo&dc&qid=1629867912&rnid=1692911031&ref=sr_pg_1']
for url in urls:
    crawling_list(url)                