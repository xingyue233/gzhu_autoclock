from requests.sessions import session
from rsa import rsa_dec, rsa_enc
import requests
import re

class URL:
    login= 'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2Fview%3Fm%3Dup'
    

def login(username, password):
    session = requests.session()
    session.cookies.clear()
    
    res = session.get(URL.login, verify=True)
    lt = re.findall(r'name="lt" value="(.*)"', res.text)

    login_form = {
        'username': username,
        'password': password,
        'ul': len(username),
        'pl': len(password),
        'lt': lt[0],
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rsa': rsa_enc(username + password + lt[0])
    }
    post_res = session.post(URL.login, data=login_form)
    if username in post_res.text:
        return [session,True]
    else:
        return [session,False]

