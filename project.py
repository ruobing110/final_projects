import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pypinyin as py

sns.set_style('whitegrid')
plt.rcParams['font.sans-serif']=['SimHei']
plt.rc('figure', figsize=(10, 10))
plt.rcParams['axes.unicode_minus']=False
sns.set(font_scale=2)

house_price = pd.read_csv('new.csv', ',', encoding= 'unicode_escape')
# remove unnecessary columns
house_price_fixed = house_price.drop(columns=['url', 'DOM','Cid', 'followers', 'buildingType', 'renovationCondition', 'constructionTime',
                                              'fiveYearsProperty', 'buildingStructure', 'ladderRatio', 'communityAverage'])

# add columns of year, month and year+month
house_price_fixed['month'] = house_price_fixed['tradeTime'].str[5:7]
house_price_fixed['month'].astype('int64')
house_price_fixed['year'] = house_price_fixed['tradeTime'].str[0:4]
house_price_fixed['year'].astype('int64')
house_price_fixed['year_month'] = house_price_fixed['tradeTime'].str[0:7]
house_price_fixed = house_price_fixed[house_price_fixed['price'] > 10000]

# print(house_price_fixed['tradeTime'].str[0:4].unique()) # check out what year is in the data
pop_l = ['2010', '2018', '2008', '2002', '2003', '2009']

for item in pop_l:
    house_remove = house_price_fixed[house_price_fixed['year'] == item] # remove the year with only a few records
    house_price_fixed = house_price_fixed.drop(labels=house_remove.axes[0])

house_price_fixed.sort_values(by=['year','month'], ascending=True, inplace=True)
house_price_fixed.reset_index(drop = True, inplace=True)


year = ['2011', '2012', '2013', '2014', '2015','2016', '2017']  # divide the data into different years

for item in year:
    yeardat = house_price_fixed[house_price_fixed['year'] == item]
    yeardat.reset_index(drop=True, inplace=True)

    f, ax = plt.subplots(figsize=(12, 15))
    sns.barplot(y="price", x='month', data=yeardat)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title( item + ' house price bar plot')
    f.savefig(item + '_house_price_bar_plot.jpg')

    f, ax = plt.subplots(figsize=(12, 15))
    sns.boxplot(y="price", x='month', data= yeardat)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(item + ' house price box plot')
    f.savefig(item + '_house_price_box_plot.jpg')

# load the rent data
def load_dataset(datasetNum):
    rent = pd.read_csv('rent'+str(datasetNum)+'.csv',sep=',')
    return rent

# combine all rent datasets
rent = []
for i in range(1,10):
    rent.append(load_dataset(i))
rent = pd.concat(rent)

# clean the data for house rent dataset
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

# reset index for rent data
rent.reset_index(inplace=True)
rent.to_csv("rentpresent.csv",index=False,sep=',')

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


f, ax = plt.subplots(figsize=(50, 15))
sns.boxplot(y="price", x='year_month', data=house_price_fixed)
ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('2011 - 2017 house price box plot')
f.savefig('2011_2017_house_price_box_plot.jpg')

f, ax = plt.subplots(figsize=(40, 15))
sns.boxplot(y='price', x='month', hue='subway', data= house_price_fixed)
plt.xlabel('Month')
plt.ylabel('Price')
plt.title('2011 - 2017 house price influenced by subway')
f.savefig('2011_2017_house_price_influenced_by_subway.jpg')

# draw histogram using rent data
rent = pd.read_csv('rentpresent.csv', ',')
rent['avg_price'] = rent['price']/rent['area']

f, ax = plt.subplots(figsize=(40, 15))
sns.kdeplot( data=rent['avg_price'], shade=True)
plt.xlabel('Rent price')
plt.ylabel('Frequency')
plt.title('House average rent price histogram')
f.savefig('House_average_rent_price_histogram.jpg')


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

