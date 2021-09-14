from bs4 import BeautifulSoup as bs
from requests import Session
import csv
s = Session()

s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

file = open("flipkart_lenovo.csv","w",newline="",encoding="utf-8")
row = csv.writer(file)

row.writerow(["Title","price","rating","image_url","Product_href"])
def crawl_list():
    for i in range(1,6):
        r = s.get(url = "https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.brand%255B%255D%3DLenovo&page={}".format(i))
        print(r)
        soup = bs(r.content,"html.parser")
        products = soup.find_all("div","_2kHMtA")
        for product in products:
            title = product.find("div","_4rR01T").text.strip()
            price = product.find("div","_30jeq3 _1_WHN1").text.strip()
            rating = ''
            if product.find("div","gUuXy-"):
                rating = product.find("div","gUuXy-").find("span").text.strip()
            product_href = product.find("a","_1fQZEK").get("href")
            image_url = product.find("img","_396cs4 _3exPp9").get("src")
            print(product.find("img","_396cs4 _3exPp9").get("src"))

            row.writerow([title,price,rating,image_url,product_href])           
    
    
crawl_list()