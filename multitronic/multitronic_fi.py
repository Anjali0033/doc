from bs4 import BeautifulSoup as bs
from time import strftime
from bs4.element import ProcessingInstruction
from requests import Session
from lxml import html
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0" 
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'multitronic'
    country = 'finland'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//div[@class="mt_well"]//h2//text()')[0]).strip()
    reg_price = ''.join(tree.xpath('//div[@id="rightWrapper"]//span[@id="vat"]//text()')).strip()
    part_no = ''.join(tree.xpath('//div[@class="greytext"]//text()')).strip().replace("ID: ","")
    model_no = ''.join(tree.xpath('//table[@class="table table-condensed"]//tr//td[contains(string(),"EAN")]//ancestor::tr//td[2]//text()'))
    stock = ''
    if tree.xpath('//div[@class="estimatedWrapper"]//span[@class="title"][contains(string(),"Currently not available ")]'):
        stock = 'stock not available'
    else:
        stock = 'stock available'    
    try:
        table = "create table multitronic_fi(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into multitronic_fi(retailer,country,extraction_date,name,reg_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into multitronic_fi(retailer,country,extraction_date,name,reg_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()        

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",stock,"\n",extraction_date,"\n=============\n")


def crawling_listpage():
    url = "https://www.multitronic.fi/en/cms/ga/action/get_product_list"
    for i in range(1,8):
        page = i
        data = {
        "adlib_item_id": "10295",
        "sort": "8",
        "sel": "0",
        "dir": "asc",
        "keywords": "Lenovo",
        "page":page,
        "ppp": "24",
        "fs": "false",
        "express": "false",
        "man": "",
        "cats": "",
        "condition_groups": "",
        "view": "2",
        "sf": "true",
        "pag": "1",
        "shop_stocks": "",
        "delivery_times": "",
        "as": "#categories_group",
        "getall": "true"
            }
        r = s.post(url=url,data=data)
        soup = bs(r.content,"html.parser")
        container = soup.find_all('div','product_description')
        for products in container:
            product_href = products.find('a','pcTracker').get('href')
            crawling_detailpage("https://www.multitronic.fi"+product_href)
            print("https://www.multitronic.fi"+product_href)

crawling_listpage()