import json
from datetime import datetime
from logging import log
from typing import Tuple
from flask import Flask, render_template,request,redirect,url_for, session
from login import login
import os

app = Flask(__name__)
dirname = os.path.dirname(__file__)
app.secret_key = '!@#$%^&*()11'
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method =='GET':
        session['user']=''
        return render_template("login.html")
        
@app.route('/login', methods=['POST'])
def userlogin():
    with open(os.path.join(dirname,'config.ini'), mode='r') as f:
        text = f.read()
        config = json.loads(text)
        f.close()
        
    username = [i['username'] for i in config]
    password = [i['password'] for i in config]  
    form = request.form.to_dict(True)
    
    res = login(form['username'], form['password'])
    if(res[1]):
        if form['username'] in username:
            session['user'] = form['username']
            return redirect('/index')
        else:
            data = {}
            data['username'] = form['username']
            data['password'] = form['password']
            data['email'] = ''
            data['status'] = 0
            session['user'] = form['username']
            config.append(data)
            output = json.dumps(config)
            with open(os.path.join(dirname,'config.ini'), mode='w') as f:
                f.write(output)
                f.close()
            return redirect('/index')
    else:
        return "<script>alert('登录失败');window.history.go(-1)</script>"
        
@app.route('/index', methods=['GET'])
def index():
    if(session.get('user')):
        with open(os.path.join(dirname,'config.ini'), mode='r') as f:
            text = f.read()
            config = json.loads(text)
            f.close()
        
        for i,j in enumerate(config):
            if j['username'] == str(session.get('user')):
                username = config[i]['username']
                password = config[i]['password']
                status = config[i]['status']
                email = config[i]['email']
        
        data = {
        'username': username,
        'password': password,
        'status': status,
        'email':email
        }
        return render_template('index.html', data=data)
    else:
        return redirect('/')
                    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    with open(os.path.join(dirname,'config.ini'), mode='r') as f:
        text = f.read()
        config = json.loads(text)
        f.close()
    
    if request.method=='GET':
        status = request.args.get('status')
        for i,j in enumerate(config):
            if j['username'] == str(session.get('user')):
                config[i]['status'] = int(status)
    else:
        form = request.form.to_dict(True)
        email = form['email']
        for i,j in enumerate(config):
            if j['username'] == str(session.get('user')):
                config[i]['email'] = email
                
    output = json.dumps(config)
    with open(os.path.join(dirname,'config.ini'), mode='w') as f:
        f.write(output)
        f.close()
        
    return redirect('/index')
            
            
        

app.run("0.0.0.0",debug=False,port=80)
