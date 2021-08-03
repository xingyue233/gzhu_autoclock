import json
from datetime import datetime
from logging import log
import re
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
def login():
    with open(os.path.join(dirname,'config.ini'), mode='r') as f:
        text = f.read()
        config = json.loads(text)
        
    username = [i['username'] for i in config]
    password = [i['password'] for i in config]  
    form = request.form.to_dict(True)
    
    res = login(form['username'], form['password'])
    
    if(res[1]):
        if form['username'] in username:
            session['user'] = username
            return redirect('/index')
        else:
            return "<script>alert('登录失败');window.history.go(-1)</script>"
        
@app.route('/index', methods=['GET'])
def index():
    if(session['user']):
        return session['user']
    else:
        return redirect('/')
                    
app.run("0.0.0.0",debug=False,port=80)
