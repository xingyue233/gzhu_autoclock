from flask.globals import request, session
from login import login
import json
import time
from datetime import datetime
from clock import clock_in
import requests
import os


dirname = os.path.dirname(__file__)

def output_msg(msg):
    timestamp = int(time.time()) + 3600 * 8
    time_format= datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    msg = "{} {}".format(msg, time_format)
    print(msg)
    with open(os.path.join(dirname,'log.txt'), mode='a+') as f:
        f.write("{}\n".format(msg))
    f.close()

output_msg("打卡系统开始启动...")

while True:
    students = {}
    
    with open(os.path.join(dirname,'config.ini'), mode='r') as f:
        text = f.read()
        config = json.loads(text)
        
    username = [i['username'] for i in config]
    password = [i['password'] for i in config]
    status = [i['status'] for i in config]
    email = [i['email'] for i in config]
    
    _datetime = ""
    now_time = int(time.time()) + 3600 * 8
    now_time_H = datetime.utcfromtimestamp(now_time).strftime('%H')
    now_time_M = datetime.utcfromtimestamp(now_time).strftime('%M')
    now_time_S = datetime.utcfromtimestamp(now_time).strftime('%S')
    with open(os.path.join(dirname,'clocktime.txt'),mode='r') as f:
        _datetime = f.read()
        f.close()
    #实时更新student和time的数据
    
    if _datetime == now_time_H and now_time_M=='00' and now_time_S=='00':
    #match the time 
        for index, statu in enumerate(status):
            if(statu):
                res = login(username[index], password[index])
                clock_in(res[0], username[index], email[index])
