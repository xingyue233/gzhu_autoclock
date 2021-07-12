from load_from_cookies import load_from_cookies
from login import login
import msession
import re
import json
import time
from datetime import datetime
import sys
import os

session = msession.session

dirname = os.path.dirname(__file__)
#clock_in.py
def helper(stu_id, days=None):
    if days:
        for day in range(days):
            clock_in(stu_id, day)
    else:
        clock_in(stu_id)

def clock_in(stu_id, days=None):
    # load_from_cookies(stu_id)

    res = session.get('http://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start')

    # get csrfToken
    csrfToken = re.findall(r'<meta itemscope="csrfToken" content="(?P<token>.*?)">', res.text)

    # before getting the URL with stepId
    form_get_url = {
        'idc': 'XNYQSB',
        'release': '',
        'csrfToken': csrfToken[0],
        'lang': 'zh'
    }
    res_get_url = session.post('http://yqtb.gzhu.edu.cn/infoplus/interface/start', data=form_get_url)

    # get URL with stepId from response
    url = json.loads(res_get_url.text)['entities'][0]

    # get json
    stepId = re.findall(r'form/(?P<id>.*?)/render', url)
    form = {
        'stepId': stepId,
        'instanceId': '',
        'admin': 'false',
        'rand': '114.514',
        'width': '1536',
        'lang': 'zh',
        'csrfToken': csrfToken[0]
    }
    session.headers.update({'referer': 'http://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start'})
    data = session.post(url='http://yqtb.gzhu.edu.cn/infoplus/interface/render', data=form)
    data_json = json.loads(data.text)['entities'][0]

    # get boundField (dummy)
    field = ''
    for key in data_json['fields']:
        field += key
        field += ','
    field = field[:-1]

    form_data = data_json['data']

    # check in ahead of schedule
    if days:
        form_data['fieldSQSJ'] += (days * 86400)

    # convert timestamp to datetime and it will be displayed later
    timestamp = form_data['fieldSQSJ'] + 8 * 3600
    _datetime = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    #get_form_fix
    formplus = {
        '_VAR_URL_Attr': '{}',
        '_VAR_URL': 'http://yqtb.gzhu.edu.cn/infoplus/form/9079843/render',
        '_VAR_ENTRY_TAGS': '疫情应用,移动端',
        '_VAR_ENTRY_NAME': '学生健康状况申报_',
        'fieldJBXXcsny': '',
        'fieldJBXXbz_Attr': '{"_parent":"Ã¨Â®Â¡Ã§Â§Â202"}',
        'fieldJBXXfdy_Attr': '{"_parent":"0206:*"}',
        'fieldjgshi_Attr': '{"_parent":"440000"}',
        'fieldJBXXjgshi_Attr': '{"_parent":"440000"}',
        'fieldJBXXjgq_Attr': '{"_parent":"440100"}',
        'fieldJBXXsheng_Name': '',
        'fieldJBXXshi_Name': '',
        'fieldJBXXshi_Attr': '{"_parent":""}',
        'fieldJBXXqu_Name': '',
        'fieldJBXXqu_Attr': '{"_parent":""}',
        'fieldSTQKfrsj': '',
        'fieldSTQKglkssj': '',
        'fieldSTQKzdkssj': '',
        'fieldSTQKzysj': '',
        'fieldSTQKpcsj': '',
        'fieldSTQKjtcyfrsj': '',
        'fieldSTQKjtcyglkssj': '',
        'fieldSTQKjtcyzdkssj': '',
        'fieldSTQKjtcyzysj': '',
        'fieldSTQKjtcypcsj': '',
        'fieldCXXXksjcsj': '',
        'fieldCXXXzhycjcsj': '',
        'fieldJCDDs_Name': '',
        'fieldJCDDshi_Name': '',
        'fieldJCDDshi_Attr': '{"_parent":""}',
        'fieldJCDDq_Name': '',
        'fieldJCDDq_Attr': '{"_parent":""}',
        'fieldYQJLksjcsj': '',
        'fieldYQJLzhycjcsj': '',
        'fieldYQJLjcdds_Name': '',
        'fieldYQJLjcddshi_Name': '',
        'fieldYQJLjcddshi_Attr': '{"_parent":""}',
        'fieldYQJLjcddq_Name': '',
        'fieldYQJLjcddq_Attr': '{"_parent":""}',
        'fieldCXXXsftjhbjtdz_Name': '',
        'fieldCXXXsftjhbs_Name': '',
        'fieldCXXXsftjhbs_Attr': '{"_parent":""}',
        'fieldCXXXsftjhbq_Name': '',
        'fieldCXXXsftjhbq_Attr': '{"_parent":""}',
        'fieldCXXXddsj': '',
        'fieldCXXXlksj': '',
        'fieldJCSJ': '',
        'fieldzgzjzdzq_Name': '',
        'fieldzgzjzdzq_Attr': '{"_parent":""}',
        'fieldzgzjzdzshi_Name': '',
        'fieldzgzjzdzshi_Attr': '{"_parent":""}',
        'fieldzgzjzdzs_Name': '',
        'fieldCXXXfxcfsj': '',
        'fieldCXXXfxxq_Name': '',
        'fieldJKMsfwlm': '1',
        'fieldYZNSFJCHS': '2',
        'fieldCNS': True
    }
    for key in formplus:
        form_data[key] = formplus[key]
    
    form = {
        'actionId': '1',
        'formData': json.dumps(form_data),
        'rand': '114.514191981',
        'remark': '',
        'nextUsers': '{}',
        'stepId': stepId,
        'timestamp': str(int(time.time())),
        'boundFields': field,
        'csrfToken': csrfToken[0],
        'lang': 'zh'
    }

    submit = session.post('http://yqtb.gzhu.edu.cn/infoplus/interface/doAction', data=form)

    if '打卡成功' in submit.text:
        output_msg ('打卡成功: {} : {}'.format(stu_id, _datetime))
    else:
        print(form_data['fieldSQSJ'])
        output_msg ('打卡失败: {} : {}'.format(stu_id, _datetime))

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
    with open(os.path.join(dirname,'users.txt'), mode='r') as f:
        for line in f:
            stu = line.split(' ')
            stu = [x.strip() for x in stu]
            students[stu[0]] = stu[1]
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
        for id in students:
            if login(id, students[id])==False:
                output_msg("{}用户名或密码错误".format(id))
            else:
                helper(id)
