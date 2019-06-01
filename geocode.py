import geocoder


# #geocod="arRTZcBxXpCOlkM9wFeX0AXGhDk4EVLl"
# g = geocoder.baidu('北京市朝阳区燕莎桥附近', key='<O8fpFPd6pw5VYK1uGsdMSAtL5MQRjAjs>')
#
# latlng = [45.3, -105.1]
# gg = geocoder.baidu(latlng, method='reverse', key='<O8fpFPd6pw5VYK1uGsdMSAtL5MQRjAjs>')
# print(gg.json)
#
# print(g.json)
# print(g.address)
# print(g.city)
# print(g.state)
# print(g.country)

import json
from urllib.request import urlopen, quote
def getBlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'O8fpFPd6pw5VYK1uGsdMSAtL5MQRjAjs'
    add = quote(address) #由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)

    # print(temp.keys())
    # print(temp.values())
    # print(type(temp['result']))


    if temp['status'] == 0 :
        lng = temp['result']['location']['lng']  # 纬度
        lat = (temp['result']['location']['lat'])  # 经度
        #print(lng, lat)
        return str(lng)+","+ str(lat)



    else:
        #print(address+"没找到")
        return "NULL"

    #输出csv
    # with open('D:\pycharm\\test_python_csv\\island\\test111.csv', 'w+', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     try:
    #         if temp['status'] == 0:
    #             lng = temp['result']['location']['lng']  # 纬度
    #             lat = (temp['result']['location']['lat'])  # 经度
    #             writer.writerow([address, lat, lng])
    #             print(00)
    #         # else:
    #         #     writer.writerow([address])
    #         #     print(11)
    #     except:
    #         print(22)
    #         writer.writerow([address])


print(getBlnglat('华南农业大学'))


