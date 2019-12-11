import pandas as pd
import json
import urllib
from urllib import request
import pypinyin as py

html = urllib.request.urlopen('http://map.amap.com/service/subway?_1573597615651&srhdata=1100_drw_beijing.json')
hjson = json.loads(html.read().decode("utf-8"))
hjson = hjson['l']


def pinyin(pinyin_list):
    content = ''
    for item in pinyin_list:
        content = content + item + ' '
    return content

subway = pd.DataFrame()
subway_s = pd.DataFrame()
# request data from website
for i in range(len(hjson)):
    line = hjson[i]     # subway line data
    line_code = hjson[i]['ls']  # line code
    name = hjson[i]['ln']   # line name
    name = py.lazy_pinyin(name) # change chinese character to pinyin
    name = pinyin(name)
    # print(name)
    order = hjson[i]['x']   # loop
    loop = hjson[i]['lo']   # loop line
    status = hjson[i]['su']     # under construction or not

    subway_line = pd.DataFrame([{'line code': line_code, 'line name': name, 'order': order,
                                 'loop': loop, 'status': status}])
    subway = pd.concat([subway, subway_line], axis=0, ignore_index= True)

    for j in range(len(line['st'])):

        station = line['st']    # station
        spinyin = station[j]['sp']  # station name
        spos = station[j]['sl']     # lat & longitude
        spos_list = spos.split(',')
        slon = spos_list[0]     # longitude
        slat = spos_list[1]     # latitude
        spass = station[j]['r']     # route passed
        strans = station[j]['t']    # transfer station
        ssu = station[j]['su']      # availability

        subway_station = pd.DataFrame([{'line code': line_code, 'line name': name,
                                        'station name': spinyin, 'longitude': slon, 'latitude': slat,
                                        'line passed': spass, 'transition': strans, 'availability': ssu}])
        subway_s = pd.concat([subway_s, subway_station], axis=0, ignore_index=True)

subway_s.to_csv('subway station.csv', index=None)
subway.to_csv('subway line.csv')
print(subway_s.head())
