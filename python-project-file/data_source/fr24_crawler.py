#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#

from typing import List, Tuple, Dict, Any
import requests,json,time,csv,os,random


class Fr24Crawler:
    def __init__(self,loc:Tuple[float, float],rng:Tuple[float, float],interval:float):
        self.loc = loc
        self.rng = rng
        self.interval = interval
        self.get_range()
        self.url = 'https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds={},{},{},{}&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=0&estimated=1&maxage=14400&gliders=1&stats=0'.format(self.maxlat,self.minlat,self.minlon,self.maxlon)


    def get_range(self):
        R_lat = abs(self.rng[0]-self.loc[0])#纬度半径
        R_lon = abs(self.loc[1]-self.rng[1])#经度半径
        self.maxlat = self.rng[0]#纬度最大
        self.minlat = self.loc[0]-R_lat#纬度最小
        self.minlon = self.rng[1]#经度最小
        self.maxlon = self.loc[1]+R_lon#经度最大


    def get_data_once(self):
        user_agent_list = ["Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.141 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"]
        header = {'user-agent': random.choice(user_agent_list)}#为了伪装浏览器以请求，防止报错
        r = requests.get(self.url,headers = header)
        raw = json.loads(r.text)#把json文件中的字符串变为python的dict与list，方便读取
        self.data_process(raw)


    def spin(self):
        if self.interval == 0:
            while True:
                time.sleep(10)
        else:
            time.sleep(self.interval)
            self.get_data_once()


    def data_process(self,raw:dict):
        del raw['full_count']
        del raw['version']
        key = ['longitude','latitude','heading','altitude','ground_speed','squawk_number','registration_number','flight_number','IATA_dep','IATA_ari']#数据的表头
        data = [key]#放在第一位（表头）
        for i in raw:
            tem_data = raw[i]
            row = []
            order = (2,1,3,4,5,6,9,13,11,12)#所需数据在list中的索引
            for j in order:
                row.append(tem_data[j])
            data.append(row)
        self.store(data)


    def store(self,data):
        if __name__ == "__main__":
            with open("./flight_data.csv","w",newline = "") as csvfile:#存为csv文件
                writer = csv.writer(csvfile)
                writer.writerows(data)
        else:
            with open("./data_source/flight_data.csv","w",newline = "") as csvfile:#存为csv文件
                writer = csv.writer(csvfile)
                writer.writerows(data)