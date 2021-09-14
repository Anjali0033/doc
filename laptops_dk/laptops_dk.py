from bs4 import BeautifulSoup as bs
from lxml import html
from time import strftime
from requests import Session, models
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
import mysql.connector
con = mysql.connector.connect(host='localhost',user='root',password='root',database='crawling',charset='utf8',use_unicode=True)
cur = con.cursor()

def crawling_detailpage(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    retailer = 'laptops'
    country = 'denmark'
    extraction_date = strftime("%A, %d %b %Y ,%r")
    name = ''.join(tree.xpath('//div[@class="product-slide-title"]//h1//text()')).strip()
    reg_price = 'Kr. '+''.join(tree.xpath('//div[@class="product-slide-price"]//text()')).replace("Kr.","").strip()
    discounted_price = ''.join(tree.xpath('//div[@class="product-slide-price-vat"]//text()')).replace("ekskl. moms)","").replace("(","").strip()
    part_no = ''.join(tree.xpath('//div[@class="box visible"]//tbody//tr//td[contains(string(),"Varenummer")]//ancestor::tr//td[2]//text()'))
    model_no = ''
    stock = ''
    if tree.xpath('//div[@class="product-slide-availability"]//span[@class="availability"]'):
        stock = 'stock available'
    elif tree.xpath('//div[@class="product-slide-availability"]//span[@class="availability yellow"]'):
        stock = 'stock not available'

    try:
        table = "create table laptops_dk(retailer varchar(100),country varchar(100),extraction_date varchar(100),name varchar(500) null,reg_price varchar(400) null COLLATE utf8_unicode_ci,discounted_price varchar(400) null COLLATE utf8_unicode_ci,part_no varchar(200) null COLLATE utf8_unicode_ci,model_no varchar(200) null COLLATE utf8_unicode_ci,stock varchar(500) null)"
        cur.execute(table)
        con.commit()
        query = "insert into laptops_dk(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit() 
    except:
        query = "insert into laptops_dk(retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        VALUES = (retailer,country,extraction_date,name,reg_price,discounted_price,part_no,model_no,stock)
        cur.execute(query,VALUES)
        con.commit()

    print("\n===========\n",part_no,"\n",model_no,"\n",name,"\n",reg_price,"\n",discounted_price,"\n",stock,"\n",extraction_date,"\n=============\n")


def crawling_listpage(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")

    for products in soup.find_all("div","catalog-main-cell"):
        product_href = products.find("a","catalog-item-img").get("href")
        crawling_detailpage("https://laptops.dk"+product_href)
        print(products.find("a","catalog-item-img").get("href"))

        

urls = ['https://laptops.dk/laptops?ItemSearchPage-useSearchV2=true&ItemSearchPage-Facet%5BStock%5D=PEStockProviderInStock&ItemSearchPage-FacetOrder%5BStock%5D%5B_term%5D=asc&ItemSearchPage-FacetValue%5BStock%5D%5B%5D=LaptopsUniconta&ItemSearchPage-Facet%5BIce_dk_Overskrift+%2F+Produktlinje%5D=Ice_dk_Overskrift+%2F+Produktlinje&ItemSearchPage-FacetOrder%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B_term%5D=asc&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X395&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520IdeaPad%25203%252017ITL6&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%252013s%2520G2%2520ITL&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%252014%2520G2%2520ARE&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%252014-IIL&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%252015%2520G2%2520ARE&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%252015%2520G2%2520ITL&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%252015-IIL&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkBook%2520Plus%2520IML&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520E14%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520E15&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520L14%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520E15%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520L15%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520L15%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P1%2520%282nd%2520Gen%29&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P1%2520Gen%25203&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P14s%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P14s%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P15%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P15s%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P15s%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P43s&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P53s&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520P53&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T14%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T14%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T14s%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T15%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T15%2520Gen%25202&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T490s&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X1%2520Yoga%2520Gen%25206&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X280&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X1%2520Carbon%2520Gen%25209&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X1%2520Nano%2520Gen%25201&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520T495s&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X1%2520Carbon%2520%287th%2520Gen%29&ItemSearchPage-FacetValue%5BIce_dk_Overskrift+%2F+Produktlinje%5D%5B%5D=Lenovo%2520ThinkPad%2520X1%2520Yoga%2520%284th%2520Gen%29']
for url in urls:
    crawling_listpage(url)