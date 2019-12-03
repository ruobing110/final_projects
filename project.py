import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pypinyin as py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression



# combine dataset
def load_dataset(datasetNum):
    rent = pd.read_csv('rent'+str(datasetNum)+'.csv',sep=',')
    return rent

rent = []
for i in range(1,10):
    rent.append(load_dataset(i))
rent = pd.concat(rent)



# clean the data
rent['price'] = rent['price'].str[0:-3]
rent['price'] = pd.to_numeric(rent.price,errors='ignore')
rent['area'] = rent['area'].str[0:-1]
rent['area'] = pd.to_numeric(rent.area,errors='ignore')
rent['housetype']=rent['housetype'].str[1:]
rent['renttype']=rent['renttype'].str[1:]
rent['renttype'] = rent['renttype'].str.replace('整租', 'not share')
rent['floor'] = rent['floor'].str.split('/',expand=True)[1]
rent['floor'] = rent['floor'].str[:-1]
rent['community'] = rent['community'].str.split('·',expand=True)[1]
rent['community'] = rent['community'].str.split(' ',expand=True)[0]
rent['longtitude'] = rent['longtitude'].str[1:-1]
rent['longtitude'] = pd.to_numeric(rent.longtitude,errors='ignore')
rent['latitude'] = rent['latitude'].str[1:-1]
rent['latitude'] = pd.to_numeric(rent.latitude,errors='ignore')


def split_housetype(column,bedroom,bathroom,livingroom):
    if len(column) == 6:
        if bedroom == True:
            return column[0]
        if bathroom == True:
            return column[4]
        if livingroom == True:
            return column[2]
    if len(column) !=6:
        if bedroom == True:
            return column[0]
        if bathroom == True:
            return column[3]
        if livingroom == True:
            return 0


rent['bedroom']= rent.apply(lambda x: split_housetype(x.housetype,True,False,False),axis=1)
rent['bathroom']= rent.apply(lambda x: split_housetype(x.housetype,False,True,False),axis=1)
rent['livingroom']= rent.apply(lambda x: split_housetype(x.housetype,False,False,True,),axis=1)
rent.drop('housetype',axis=1,inplace=True)


def pinyin(pinyin_list):
    content = ''
    for item in pinyin_list:
        content = content + item + ' '
    return content
rent['community'] = rent.apply(lambda x:pinyin(py.lazy_pinyin(x.community)),axis = 1)


subway = pd.read_csv('subway station.csv',sep=',')


rent.reset_index(inplace=True)

def getdisfromXtoY(lng_a,lat_a,lng_b,lat_b):
        pk = 180/3.14169
        a1 = lat_a/pk
        a2 = lng_a / pk
        b1 = lat_b / pk
        b2 = lng_b / pk
        t1 = np.cos(a1)* np.cos(a2) * np.cos(b1) *np.cos(b2)
        t2 = np.cos(a1)*np.sin(a2) *np.cos(b1) *np.sin(b2)
        t3 = np.sin(a1)*np.sin(b1)
        tt = np.arccos(t1 + t2 + t3)
        return 6378000*tt



for i in rent.index:
    result = getdisfromXtoY(rent['longtitude'][i],rent['latitude'][i],subway['longitude'],subway['latitude'])
    pos1 = result.sort_values().index[0]
    subwayname = subway.loc[pos1,'station name']
    distance = np.min(result)
    rent.loc[i,'match station'] = subwayname
    rent.loc[i,'distance'] = distance


rent['avg_price'] = rent['price']/rent['area']
rent.to_csv("rentfinal.csv",index=False,sep=',')


rent = pd.read_csv('rentfinal.csv',sep=',')

rent1 = rent[rent['distance']<2000]
rent_plot = rent[rent['distance']<5000]
sns.jointplot(x='distance',y='avg_price',kind='hex',color='k',data=rent_plot)
plt.subplots(figsize=(10,10))
sns.regplot(x='distance',y='avg_price',data=rent_plot)
plt.show()


def cut_distance(x):
    if x < 1000:
        return 1
    if 1000 <= x <2000:
        return 2
    if 2000 <= x < 3000:
        return 3
    if 3000 <= x < 4000:
        return 4
    if 4000 <= x < 5000:
        return 5
    if 5000 <= x < 6000:
        return 6


rent['cut_distance'] = rent.apply(lambda x: cut_distance(x.distance), axis = 1)


sns.set(font_scale=2)
f, ax = plt.subplots(figsize=(20, 15))
sns.boxplot(y='avg_price', x='cut_distance', data= rent)
plt.xlabel('distance(km)')
plt.ylabel('Average Price(yuan/m2)')
plt.title('2011 - 2017 house rent price influenced by subway')
plt.show()



rent2 = rent[rent['distance']<1000]
rent3= rent1[rent1['distance']>1000]
m_1 = rent2['avg_price'].mean(0)
m_2 = rent3['avg_price'].mean(0)
print(m_1)
print(m_2)

avg_area = rent['area'].mean(0)
print(avg_area)
print(m_1*avg_area)
print(m_2*avg_area)

print(rent2['price'].mean(0))
print(rent3['price'].mean(0))


lrModel = LinearRegression()
#(3) 接着，我们把自变量和因变量选择出来
x = rent1[['distance']]
y = rent1[['avg_price']]

#模型训练


print(lrModel.fit(x,y))


#对回归模型进行检验
print(lrModel.score(x,y))
a = lrModel.intercept_
b = lrModel.coef_
a = float(a)
b = float(b)
print('y = {} + {} * x'.format(a, b))





