from datetime import datetime
import time
import os
now_time = int(time.time()) + 3600 * 8
now_time_H = datetime.utcfromtimestamp(now_time).strftime('%H')
now_time_M = datetime.utcfromtimestamp(now_time).strftime('%M')
now_time_S = datetime.utcfromtimestamp(now_time).strftime('%S')
print(now_time_M, now_time_S)
dirname = os.path.dirname(__file__)

while True:
    _datetime = ""
    now_time = int(time.time()) + 3600 * 8
    now_time_H = datetime.utcfromtimestamp(now_time).strftime('%H')
    now_time_M = datetime.utcfromtimestamp(now_time).strftime('%M')
    now_time_S = datetime.utcfromtimestamp(now_time).strftime('%S')
    with open(os.path.join(dirname,'clocktime.txt'),mode='r') as f:
        _datetime = f.read()
        f.close()
    #实时更新student和time的数据
    print(now_time_H, _datetime) 
    if _datetime == now_time_H and now_time_M=='54' and now_time_S=='00':
    #match the time 
        print(1)
        
    
