import requests 
import json
import time
headers = {'user-agent': 'sdf'}
r = requests.get('https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds=31.53,30.90,120.91,122.17&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=14400&gliders=1&stats=0',headers=headers)
raw = json.loads(r.text)
del raw['full_count']
del raw['version']
'''
According to the response of the url, the python dict, which is coverted from the responsed json file, has two keys "full_count" and "version". Key "full_count" shows
the number of all the flights in the world and key "version" shows the version of it. These two keys are not related to the detailed flight data we need
'''
key = []
for i in raw:
    key.append(i)
length = len(raw[key[0]]) 
explanation = [
    'For value"0", we consider it as  ICAO-24bit address, because we directly see the ICAO-24bit address which is provided on the website, by comparing the value, we can know the ICAO-24bit address is equal to value"0".',
    'For value"1", we consider it as latitude, because the value in value"1" are all in the range between 30.90 and 31.53.',
    'For value"2", we consider it as longitude, because the value in value"2" are all in the range between 120.91 and 122.17.',
    'For value"3", we consider it as track, because we directly see the track which is provided on the website, by comparing the value, we can know the track is equal to value"3".',
    'For value"4", we consider it as altitude, because we directly see the altitude which is provided on the website, by comparing the value, we can know the altitude is equal to value"4".',
    'For value"5", we consider it as ground speed, because we directly see the ground speed which is provided on the website, by comparing the value, we can know the ground speed is equal to value"5".',
    'For value"6", we consider it as squawk number, although the squawk number is not provided by the website for free, we can see the types of all the values in value"6" are string, and all the strings are four numbers. We can guess that the four numbers are the squawk number, because we already knows that "7700" is the squawk number for mechanical fault from the movie 《中国机长》. We can also know that squawk number is always four numbers by searching the Internet. So by guessing, the squawk number is equal to value"6".',
    'For value"7", we consider it as the type of radar, by searching the Internet, we can now that this part of data shows the type of radar used to communicate with the flight. And from the website we can know that the type is chosen in all the receivers that detect the flights.',
    'For value"8", we consider it as the type of the airplane, by comparing the data on the website UI, searching the Internet and common knowledge, for example, "A320" and "A321" are common type of the airplanes, we can now that this part of data display the type of the airplane.',
    'For value"9", we consider it as registration , by comparing the data on the website UI, we can now that this part of data display the registration of the airplane.',
    'For value"10", we consider it as the last time stamp when radars detected the flight, by changing the timestamp into local time, we can see that the local time is close to the time we request the url, it also changes when we requests again. So our team guess that this part of data shows the last time the website detect the airplane.',
    'For value"11", we consider it as departure airport’s IATA, by comparing the data on the website UI, we can now that this part of data display the IATA of the departure airport of the airplane.',
    'For value"12", we consider it as arrival airport’s IATA, by comparing the data on the website UI, we can now that this part of data display the IATA of the departure airport of the airplane.',
    'For value"13", we consider it as flight number(IATA), by comparing the data on the website UI, we can now that this part of data display the flight number of the airplane and the airline company is shown in IATA code.',
    'For value"14", we consider it as whether the airplane is landed，1 stands for landed，0 stands for in-air, by comparing the other data of the flights, we can see that the flight with value"14" is 1 all have 0 in altitude and the flight with value"14" is 0 all have positive values in value"14". So our team guess this part of data shows whether the airplane is on the ground.',
    'For value"15", we consider it as the rate of climb of the airplane, by comparing data shown on the flightradar24 website UI and the data on the flightaware website UI, we can know that this part of data shows that the rate of climb of the airplane, and the unit of the data is miles per minute',
    'For value"16", we consider it as flight number(ICAO), by comparing the data in value"13", the only change is the letters before the numbers. By searching, the three letters(ICAO) and two letters(IATA) both mean one airline company. So this part of data also means the flight number and the airline company is shown in ICAO code.',
    'For value"17”, we guess it is a kind of status code for a flight，0 stands for normal，1 stands for abnormal, it is totally a guess, because we can not find the data that this part of value is "1". And we can only find "0" data in this part.',
    'For value"18", we consider it as the ICAO code of the airline company of the flight, according to the value"13" and the Internet, we can know that this part of data shows the ICAO code of the airline company of the flight.'
]
for k in range(length):
    temp = []
    for j in key:
        temp.append(raw[j][k])
    print('value"{}"'.format(k)+':',temp)
    if k == 10:
        print("时间戳转化如下：")
        for i in temp:
            a = time.localtime(i)
            time_str = time.strftime("%Y-%m-%d %H:%M:%S",a)
            print(time_str)
    print(explanation[k])
    print()