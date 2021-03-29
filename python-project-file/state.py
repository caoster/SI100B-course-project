#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#
from typing import Tuple
from data_source.fr24_crawler import Fr24Crawler
from light_controller.controller import BaseController
import csv,multiprocessing,time,os


class State:

    def __init__(self):
        self.pin26 = BaseController(None,None).pre_load(26)
        self.pin19 = BaseController(None,None).pre_load(19)
        self.pin7 = BaseController(None,None).pre_load1(7)
        self.pin8 = BaseController(None,None).pre_load1(8)
        BaseController(self.pin7,0)
        BaseController(self.pin8,0)
        BaseController(self.pin19,0)
        BaseController(self.pin26,0)
        pass


    def spin(self,loc_lat=31.17940,loc_lon=121.59043,rng_lat=32.67940,rng_lon=120.09043,interval=10,mode=1):
        crawler1 = Fr24Crawler((loc_lat,loc_lon),(rng_lat,rng_lon),interval)
        latitude_length = abs(loc_lat-rng_lat)*2
        longtitude_length = abs(loc_lon-rng_lon)*2
        last_modified_time1 = os.stat("./data_source/status.csv").st_mtime
        try:
            while True:
                if os.stat("./data_source/status.csv").st_mtime != last_modified_time1:
                    last_modified_time1 = os.stat("./data_source/status.csv").st_mtime
                    with open("./data_source/status.csv","r") as f:
                        reader = csv.reader(f)
                        reader = list(reader)
                        for i in range(5):
                            reader[0][i] = float(reader[0][i])
                        mode = int(reader[0][5])
                    crawler1 = Fr24Crawler((reader[0][0],reader[0][1]),(reader[0][2],reader[0][3]),reader[0][4])
                    latitude_length = abs(reader[0][0]-reader[0][2])*2
                    longtitude_length = abs(reader[0][1]-reader[0][3])*2
                crawler1.spin()
                with open("./data_source/flight_data.csv","r") as f:
                    reader = csv.reader(f)
                    l1 = list(reader)
                l1.pop(0)
                self.density = len(l1)/(latitude_length*longtitude_length)
                self.speed_num = 0
                self.altitude_num = 0
                for i in l1:
                    if float(i[4]) > 100:
                        self.speed_num += 1
                    if float(i[3]) > 5000:
                        self.altitude_num += 1
                print(self.density,self.speed_num/(latitude_length*longtitude_length),self.altitude_num/(latitude_length*longtitude_length))
                self.density = int(self.density / 0.04)
                self.speed_num = int((self.speed_num/(latitude_length*longtitude_length))/0.04)
                self.altitude_num = int((self.altitude_num/(latitude_length*longtitude_length))/0.04)
                if mode == 1:
                    self.control(self.density)
                elif mode == 2:
                    self.control(self.speed_num)
                elif mode == 3:
                    self.control(self.altitude_num)
        except KeyboardInterrupt:
            raise KeyboardInterrupt


    def control(self,control_data):
        if control_data >= 625:
            control_data = 624
        light_pin7 = ((control_data // 5) // 5) // 5
        light_pin8 = ((control_data // 5) // 5) % 5
        light_pin19 = (control_data // 5) % 5
        light_pin26 = control_data % 5
        print("answer:"+str(light_pin7)+str(light_pin8)+str(light_pin19)+str(light_pin26))
        BaseController(self.pin7,light_pin7)
        BaseController(self.pin8,light_pin8)
        BaseController(self.pin19,light_pin19)
        BaseController(self.pin26,light_pin26)

if __name__ == "__main__":
    a = State()
    a.spin()