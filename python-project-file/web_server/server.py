
#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#
import sys,os,csv,matplotlib,math
matplotlib.use("Agg")
from flask import Flask, request, render_template, redirect, url_for
from matplotlib import pyplot as plt


loc_lat = 31.17940
loc_lon = 121.59043
rng_lat = 32.67940
rng_lon = 120.09043
interval = 10.0
model = 1
web_server = Flask(__name__)
web_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@web_server.route('/',methods=['GET'])
def home():
    global model1,direct1,direct2,direct3,direct4 
    if model == 1:
        model1 = "表示飞机密度"
    elif model == 2:
        model1 = "表示地速大于100的飞机数量"
    elif model == 3:
        model1 = "表示高度大于5000的飞机数量"
    if loc_lat > 0:
        direct1 = "N"
    elif loc_lat < 0:
        direct1 = "S"
    else:
        direct1 = ""
    if loc_lon > 0:
        direct2 = "E"
    elif loc_lon < 0:
        direct2 = "W"
    else:
        direct2 = ""
    if rng_lat > 0:
        direct3 = "N"
    elif rng_lat < 0:
        direct3 = "S"
    else:
        direct3 = ""
    if rng_lon > 0:
        direct4 = "E"
    elif rng_lon < 0:
        direct4 = "W"
    else:
        direct4 = ""
    return render_template('home page.html',data1=loc_lat,data2=loc_lon,data3=rng_lat,data4=rng_lon,data5=interval,data6=model1,direction1=direct1,direction2=direct2,direction3=direct3,direction4=direct4)


@web_server.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return redirect(url_for("/"),code=302)
    try:
        global loc_lat,loc_lon,rng_lat,rng_lon,interval,model
        float(request.form.get('data_loc_lat'))
        float(request.form.get('data_loc_lat'))
        float(request.form.get('data_rng_lat'))
        float(request.form.get('data_rng_lon'))
        float(request.form.get('interval'))
        loc_lat = float(request.form.get('data_loc_lat'))
        loc_lon = float(request.form.get('data_loc_lon'))
        rng_lat = float(request.form.get('data_rng_lat'))
        rng_lon = float(request.form.get('data_rng_lon'))
        interval = float(request.form.get('interval'))
        model = int(request.form.get('model'))
        status = [loc_lat,loc_lon,rng_lat,rng_lon,interval,model]
        if __name__ == "__main__":
            with open("./../data_source/status.csv","w",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(status)
        else:
            with open("./data_source/status.csv","w",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(status)
    except ValueError:
        return render_template('home page.html',data1=loc_lat,data2=loc_lon,data3=rng_lat,data4=rng_lon,data5=interval,data6=model1,direction1=direct1,direction2=direct2,direction3=direct3,direction4=direct4,error="请输入正确坐标")
    return render_template("handler.html",title="Succeeded",handler="传入参数成功")


@web_server.route('/vis', methods=['GET'])
def vis():
    sorting = []
    altitude = []
    flight_number = []
    if __name__ == "__main__":
        with open('./../data_source/flight_data.csv') as f:
            reader = list(csv.reader(f))
            reader.pop(0)
            for line in reader:
                sorting.append((float(line[0]),float(line[1]),((90-int(line[2]))/360)*2*math.pi))
                altitude.append(float(line[3]))
                flight_number.append(str(line[-3]))
    else:
        with open('./data_source/flight_data.csv') as f:
            reader = list(csv.reader(f))
            reader.pop(0)
            for line in reader:
                sorting.append((float(line[0]),float(line[1]),((90-int(line[2]))/360)*2*math.pi))
                altitude.append(float(line[3]))
                flight_number.append(str(line[-3]))
    sorted_longtitude = []
    sorted_latitude = []
    arrow_x = []
    arrow_y = []
    for i in sorting:
        sorted_longtitude.append(i[0])
        sorted_latitude.append(i[1])
        arrow_x.append(math.cos(i[2]))
        arrow_y.append(math.sin(i[2]))
    plt.figure(figsize=(12, 9))
    for i in range(len(flight_number)):
        plt.quiver(sorted_longtitude[i], sorted_latitude[i], arrow_x[i], arrow_y[i], scale=65, color="b",alpha=0.5)
        a = plt.scatter(sorted_longtitude[i], sorted_latitude[i], s=10, marker="o", c="b")
        plt.text(sorted_longtitude[i]+0.025, sorted_latitude[i]+0.025, flight_number[i], size=6.5, bbox=dict(boxstyle="round",fc="cyan",ec="black",alpha=0.5))
    a.set_label("flight")
    plt.legend()
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.axis("equal")
    plt.title('Flights shown by longitude and latitude')
    if __name__ == "__main__":
        plt.savefig('./static/image.jpeg')
    else:
        plt.savefig('./web_server/static/image.jpeg')
    plt.close()
    chart = {'0': 0, '1 ~ 10000': 0, '10001 ~ 20000': 0, '20001 ~ 30000': 0, '30000+': 0}
    for al in altitude:
        if al == 0:
            chart['0'] += 1
        elif al <= 10000:
            chart['1 ~ 10000'] += 1
        elif al <= 20000:
            chart['10001 ~ 20000'] += 1
        elif al <= 30000:
            chart['20001 ~ 30000'] += 1
        else:
            chart['30000+'] += 1
    labels = []
    values = []
    for i in chart:
        labels.append(i)
        values.append(chart[i])
    plt.figure(figsize=(12,9))
    plt.xlabel('')
    plt.ylabel('')
    plt.pie(values,labels=labels,autopct='%1.1f%%',startangle=90,counterclock=False)
    plt.title('The proportion of flights by altitude')
    if __name__ == "__main__":
        plt.savefig('./static/image1.jpeg')
    else:
        plt.savefig('./web_server/static/image1.jpeg')
    plt.close()
    return render_template('vis.html')


@web_server.route("/nothing")
def nothing():
    return "nothing here! :("


if __name__ == "__main__":
    web_server.env = "development"
    web_server.debug = True
    web_server.run(host="127.0.0.1",port=5000)
