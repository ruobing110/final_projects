import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    f.savefig(item + 'house price bar plot.jpg')

    f, ax = plt.subplots(figsize=(12, 15))
    sns.boxplot(y="price", x='month', data= yeardat)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(item + ' house price box plot')
    f.savefig(item + 'house price box plot.jpg')

f, ax = plt.subplots(figsize=(50, 15))
sns.boxplot(y="price", x='year_month', data=house_price_fixed)
ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('2011 - 2017 house price box plot')
f.savefig('2011_2017 house price box plot.jpg')

f, ax = plt.subplots(figsize=(40, 15))
sns.boxplot(y='price', x='month', hue='subway', data= house_price_fixed)
plt.xlabel('Month')
plt.ylabel('Price')
plt.title('2011 - 2017 house price influenced by subway')
f.savefig('2011_2017 house price influenced by subway.jpg')

# draw histogram using rent data
rent = pd.read_csv('rentpresent.csv', ',')
rent['avg_price'] = rent['price']/rent['area']

f, ax = plt.subplots(figsize=(40, 15))
sns.kdeplot( data=rent['avg_price'], shade=True)
plt.xlabel('Rent price')
plt.ylabel('Frequency')
plt.title('House average rent price histogram')
f.savefig('House average rent price histogram.jpg')

