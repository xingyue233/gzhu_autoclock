import json
import time
import os
from datetime import datetime
from flask import Flask , render_template,request



app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method =='GET':
        students = {}
        with open('users.txt', mode='r') as f:
                    for line in f:
                        stu = line.split(' ')
                        stu = [x.strip() for x in stu]
                        students[stu[0]] = stu[1]
        f.close()
        with open('clocktime.txt',mode='r') as f:
            _datetime = "{}:00:00".format(f.read())
        f.close()
        return render_template("index.html",users=students,datetime=_datetime)

    if request.method == 'POST':
        request.args.to_dict()
        data = request.form
        option = data['submit']
        if option == '添加账号':
            with open('users.txt', mode='a+') as f:
                f.write("{} {}\n".format(data['username'],data['password']))
            return "<script>alert('{}');window.location.href='./'</script>".format(data['username'] + "添加成功")

        if option == '修改打卡时间':
            with open('clocktime.txt', mode='w') as f:
                f.write(data['h'])
            return "<script>alert('将于每天{}时00分00秒进行自动打卡');window.location.href='./'</script>".format(data['h'])

        if option == '查看系统运行状态':
            with open('log.txt', mode='r') as f:
                data = f.read()
                _split = data.split('\n')
                data_format = ""
                for i in _split:
                    data_format += i + "<br>"
                return data_format
            
app.run("0.0.0.0",debug=False,port=80)
