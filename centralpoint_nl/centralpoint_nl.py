from bs4 import BeautifulSoup as bs
from requests import Session
import csv
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"

file = open("centralpoint.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)

row.writerow(["Title","Price excl. btw","price incl. btw","Code","product_href"])
def detail_page(product_href): 
    r = s.get(product_href)
    soup = bs(r.content,"html.parser")
    price2 = soup.find("span","product-order__price-incl-text-number").text.strip()
    return price2
    

def Crawl_List(url):
    r = s.get(url)
    soup = bs(r.content,"html.parser")
    products = soup.find_all("div","card landscape wide")

    for product in products:
        name = product.find("div","title").text.strip()
        product_href = product.find("div","title").find("a").get("href")
        print(product_href)
        price2 = detail_page(product_href)
        code = product.find("div","productNumber").text.replace(")","").replace("(","").strip()
        price1 = product.find("div","price priceExcl").text.strip().replace(" excl. btw","")   

        row.writerow([name,price1,price2,code,product_href])           
    if soup.find("a","button lightBlue more next"):
        url_page = soup.find("a","button lightBlue more next").get("href")
        if(url.startswith("https://www.centralpoint.be")):
            Crawl_List("https://www.centralpoint.be"+url_page)
        else:
            Crawl_List("https://www.centralpoint.nl"+url_page)
    

urls=["https://www.centralpoint.be/nl/all-in-one-pcs-workstations/?cat=all-in-one-pcs-workstations&page=category&reset=1&searchVendors=Lenovo","https://www.centralpoint.be/nl/pcs-werkstations/?cat=pcs-werkstations&page=category&reset=1&searchVendors=Lenovo","https://www.centralpoint.be/nl/laptops/?cat=laptops&page=category&reset=1&searchVendors=Lenovo","https://www.centralpoint.nl/notebooks-laptops/?sf=1&reset=1&searchVendors=Lenovo","https://www.centralpoint.nl/pcs/?sf=1&reset=1&searchVendors=Lenovo&reset=1&searchVendors=Lenovo","https://www.centralpoint.nl/tablets/?cat=tablets&sf=1&reset=1&searchVendors=Lenovo"]
for url in urls:
    Crawl_List(url)
    