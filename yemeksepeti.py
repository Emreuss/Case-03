from dataclasses import replace
from selenium import webdriver
from soupsieve import comments
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import  BeautifulSoup
import pandas as pd 
import ast
from sqlalchemy import create_engine

driver_path = "./chromedriver"
engine = create_engine('postgresql://postgres:Pa55w.rd@localhost:5432/yemeksepetidb')
restaurant_url=engine.execute("SELECT url_rst FROM restaurant_url")
url_info=[]
driver_service = Service(executable_path=driver_path)
browser=webdriver.Chrome(service=driver_service)

for url in restaurant_url:
    url_info.append(url[0])

print(url_info)
print(len(url_info))
print(url_info[0])
comments=[]
genel=[]
Points = []
pagecommentlink= []

for url_rst in range(0,len(url_info)):
    firma_url=url_info[url_rst]
    browser.get(firma_url)
    content = browser.page_source
    soup=BeautifulSoup(content,"lxml")
    for a_href in soup.find_all("a", href=True):
        if a_href["href"].find(firma_url[28:]) == 1:
            pagecommentlink.append("https://www.yemeksepeti.com/" + a_href["href"])
for element in range(0,len(pagecommentlink)):
    print("Comment'ler yazılıyor......")
    print(pagecommentlink[element])
    browser.get(pagecommentlink[element])
    content = browser.page_source
    soup=BeautifulSoup(content,"lxml")
    for element in soup.find_all('div',{'class':'comment row'}):
        name = element.find('p')
        if name not in comments:
            comments.append(name.text)
            comments_df= pd.DataFrame({'comment':comments})
            comments_df["restaurant_name"] = browser.title
            comments_df.to_sql('restaurant_comments',engine,if_exists='append',index=False)


for element in range(0,len(pagecommentlink)):
    print("Puanlar yazılıyor......")
    print(pagecommentlink[element])
    browser.get(pagecommentlink[element])
    content = browser.page_source
    soup=BeautifulSoup(content,"lxml")
    for element in soup.find_all('div',{'class':'restaurantPoints col-md-12'}):
        points= ast.literal_eval('{'+element.text.replace('|',',') \
               .replace('Hız',"'speed_point'") \
               .replace('Servis',"'service_point'") \
              .replace('Lezzet',"'flavor_point'") \
              .replace('"','') + '}')
        Points.append(points)
        Point_df=pd.DataFrame(Points)
        Point_df["restaurant_name"]=browser.title
        Point_df.to_sql('restaurant_point',engine,if_exists='append',index=False)
