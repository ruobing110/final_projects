import requests
import re
from bs4 import BeautifulSoup
import pandas as pd



# 获取链家网连接
headers={
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}


# #获取每个页面租房信息的Url
def gethouseUrl(pageNumber):
    houseurl = []
    pageurl = "https://bj.lianjia.com/zufang/" +  'pg%s/#contentList' % pageNumber
    html = requests.get(pageurl,headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    titles = soup.find_all(class_='content__list--item--title twoline')
    for i in range(len(titles)):
        url = titles[i].a['href']
        url = "https://bj.lianjia.com" + url
        houseurl.append(url)
    return houseurl


# get detailed information for longtitude and latitude

def get_location(url):
    sub = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(sub.text, 'html.parser')
    lon_lat = soup1.select('script')[5].text
    regex_lon = 'longitude:(.*)'
    regex_lat = 'latitude:(.*)'
    lon = re.search(regex_lon, lon_lat)
    lat = re.search(regex_lat, lon_lat)
    lon = str(lon).split(':')[1][1:-3]
    lat = str(lat).split(':')[1][1:-2]
    return lon,lat


def get_info(houseurl):
    detail = {}
    response = requests.get(houseurl, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        b = soup.find("div", class_="content__list--item")
        detail["price"] = (soup.find( class_="content__aside--title")).text.strip().split('\n')[0]
        b = soup.find(class_="content__aside__list").text.strip().split('\n')
        detail["area"] = b[1].split(' ')[1]
        detail['renttype'] = b[0].split(':')[0][4:]
        detail['housetype'] = b[1].split(' ')[0][4:]
        detail['floor'] = b[2].split(' ')[1]
        detail["community"] =(soup.find(class_="content__title")).text.strip()
        detail['longtitude'] = get_location(houseurl)[0]
        detail['latitude'] = get_location(houseurl)[1]
    return detail

eachrow= []
for i in range(99):
    houseurl = gethouseUrl(i)
    for url in houseurl:
        info = get_info(url)
        print(info)
        eachrow.append(info)

dataframe = pd.DataFrame(eachrow)
print(dataframe)

dataframe.to_csv("testfinal.csv",index=False,sep=',')