from bs4 import BeautifulSoup as bs
from lxml import html
from time import strftime
from requests import Session
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'microspot'
    country = 'sw/germany'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//h1[@class="_3L3q2V Qmn5eI UYdIqI"]//text()'))
    reg_price = ''.join(tree.xpath('//div[@class="cS5hj4 _3chBkw"]//span[2]//text()'))
    part_no = ''.join(tree.xpath('//div[@class="_3i5YKg"]//text()')).replace("Artikel-Nr ","")
    model_no = ''.join(tree.xpath('//p[@class="tV_kFr"]//text()')).replace("Hersteller-Nr. ","")
    stock = ''
    if tree.xpath('//div[@class="wQ1zdx _16IhhM"]//span[@class="_10kEir"][contains(string(),"Lieferung voraussichtlich")]'):
        stock = "shock availble"
    elif tree.xpath('//div[@class="wQ1zdx _16IhhM"]//span[@class="_10kEir"][contains(string(),"Lieferung auf Bestellung")]'):
        stock= "stock not available"


    try:
        table = "create table microspot_ch_de(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into microspot_ch_de(retailer,country,extraction_date,name,reg_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into microspot_ch_de(retailer,country,extraction_date,name,reg_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",stock,"\n",extraction_date,"\n=============\n")



def crawling_listpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    soup = bs(r.content,"html.parser")

    for products in soup.find_all("div","wQ1zdx _22abxI _2tZgGy _1ryioq"):
        product_href = products.find("a","_2FaHUU").get("href")
        print(products.find("a","_2FaHUU").get("href"))
        crawling_detailpage("https://www.microspot.ch"+product_href)

    if tree.xpath('//ul[@class="_4GVcF0"]//li[@class="K2DOit"]//a[@class="_16Ool9"]//button[@class="_3tjBsa _1qTCBs KDDAjc _3GAH1f"]//span[contains(string(),"Weiter")]'):
        url_page = ''.join(tree.xpath('//ul[@class="_4GVcF0"]//li[@class="K2DOit"]//a[@class="_16Ool9"]//button[@class="_3tjBsa _1qTCBs KDDAjc _3GAH1f"]//span[contains(string(),"Weiter")]//ancestor::a//@href'))
        print(tree.xpath('//ul[@class="_4GVcF0"]//li[@class="K2DOit"]//a[@class="_16Ool9"]//button[@class="_3tjBsa _1qTCBs KDDAjc _3GAH1f"]//span[contains(string(),"Weiter")]//ancestor::a//@href'))
        crawling_listpage("https://www.microspot.ch"+url_page)
        

urls = ['https://www.microspot.ch/de/computer-gaming/notebooks/notebooks--c511000?brand=LENOVO&page=1']
for url in urls:
    crawling_listpage(url)