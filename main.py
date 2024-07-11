from flask import Flask, request, jsonify,render_template, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import mysql.connector
from datetime import datetime
import requests
import re
from flask_cors import CORS
from flask_turnstile import Turnstile
import extra
import time
# import json

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per second"], 
    # storage_uri='redis://192.168.31.6:6379'
)
# redis_client = redis.Redis(host='192.168.31.6', port=6379, db=0)
DATABASE = {
    'host': '127.0.0.1',
    'user': 'gtdata',
    'password': 'xxxxxxxx',
    'database': 'gtdata'
}
# 加载cookies


app = Flask(__name__)
CORS(app)
limiter.init_app(app)
app.config.update(
    TURNSTILE_ENABLED = True,
    TURNSTILE_SITE_KEY = "0x4AAxxxxxxca7Y",
    TURNSTILE_SECRET_KEY = "0x4AAAAAAxxxx57I7mNe8sY"
)

turnstile = Turnstile(app=app)

text1 = ''')]}'

[["wrb.fr","MkEWBc","[[null,null,\\"en\\",[[[0,[[[null,72]],[true]]]],72],[[\\"Please go to https://gt.hzchu.top/ipcheck/ to complete the verification.\\",null,null,72]],null,[\\"Please go to https://gt.hzchu.top/ipcheck/ to complete the verification.\\",\\"auto\\",\\"zh-CN\\",true]],[[[null,\\"Qǐng fǎngwèn https://Gt.Hzchu.Top/ipcheck/wánchéng yànzhèng.\\",null,null,null,[[\\"请访问https://gt.hzchu.top/ipcheck/完成验证。\\",null,null,null,[[\\"请访问https://gt.hzchu.top/ipcheck/完成验证。\\",[5],[]],[\\"请访问https://gt.hzchu.top/ipcheck/以完成验证。\\",[11],[]]]]],null,null,null,[]]],\\"zh-CN\\",1,\\"en\\",[\\"Please go to https://gt.hzchu.top/ipcheck/ to complete the verification.\\",\\"auto\\",\\"zh-CN\\",true]],\\"en\\"]",null,null,null,"generic"],["di",218],["af.httprm",217,"784462372455984077",2]]'''
text2 = ''')]}'

[["wrb.fr","MkEWBc","[[null,null,\\"en\\",[[[0,[[[null,98]],[true]]]],98],[[\\"the usage times are insufficient, please go to https://gt.hzchu.top/ipaddtimes/ to add usage times..\\",null,null,98]],null,[\\"the usage times are insufficient, please go to https://gt.hzchu.top/ipaddtimes/ to add usage times..\\",\\"auto\\",\\"zh-CN\\",true]],[[[null,\\"Shǐyòng cì shǔ bùzú, qǐng qiánwǎng https://Gt.Hzchu.top/ipaddtimes/tiānjiā shǐyòng cìshù.\\",null,null,null,[[\\"使用次数不足，请前往https://gt.hzchu.top/ipaddtimes/添加使用次数。\\",null,null,null,[[\\"使用次数不足，请前往https://gt.hzchu.top/ipaddtimes/添加使用次数。\\",[5],[]],[\\"使用次数不足，请到https://gt.hzchu.top/ipaddtimes/添加使用次数。\\",[11],[]]]]],null,null,null,[]]],\\"zh-CN\\",1,\\"en\\",[\\"the usage times are insufficient, please go to https://gt.hzchu.top/ipaddtimes/ to add usage times..\\",\\"auto\\",\\"zh-CN\\",true]],\\"en\\"]",null,null,null,"generic"],["di",311],["af.httprm",310,"2817332122764937396",77]]'''

@app.route('/_/TranslateWebserverUi/data/batchexecute', methods=['POST'])
def translate_process():
    #user_ip = get_remote_address()
    user_ip = request.headers['X-Real-Ip']
    user_input_cookies = request.cookies
    times, addtimes, checked, addtime, lastusetime = getipinfo(user_ip)
    # print(check_ip)
    if checked != 1:
        return text1
    
    if times >= 1000*(addtimes+1):
 
        return text2
    
    body = request.get_data(as_text=True)
    # print(body)

    if user_input_cookies:
        work_cookies = processcookies(user_input_cookies)
        # 保存cookies到文件
        # with open('cookies.txt', 'w') as f:
            # json.dump(user_input_cookies, f)
        # print(work_cookies)
        
    else:
        work_cookies = cookies
        # print(work_cookies)

    res = requests.post('https://translate.google.com/_/TranslateWebserverUi/data/batchexecute', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Referer': 'https://translate.google.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }, data=body,cookies=work_cookies)



    httpcode = res.status_code
    # redis_client.incr('times')
    conn = None
    try:
        conn= mysql.connector.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute('UPDATE alltimes SET times = times + 1')
        
        cur.execute(f"INSERT INTO user (ip, times, lastusetime) VALUES ('{user_ip}', 1, NOW()) ON DUPLICATE KEY UPDATE times = times + 1, lastusetime = NOW();")
        # cur.execute('UPDATE times SET count = count + 1 WHERE id = 1')
        conn.commit()
    finally:
        if conn:
            conn.close()
    # print(res.text)
    
    # time.sleep(3000)
    return res.text, httpcode

@app.route('/ipaddtimes/')
def ipaddtimes_web():
  return render_template('ipaddtimes.html')

@app.route('/ipcheck/')
def ipcheck_web():
  return render_template('ipcheck.html')

@app.route('/')
def root_web():
  return render_template('index.html')

@app.route('/_api/status')
def get_status():
    conn = None
    try:
        conn= mysql.connector.connect(**DATABASE)
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT * FROM alltimes")
        conn.commit()
        result = cur.fetchall()
    finally:
        if conn:
            conn.close()

    json = {
        "code": 0,
        "times": result[0][0]
    }
    
    return jsonify(json), 200

@app.route('/_api/check')
def translate_check():
    body = {
        'f.req': '[[["rPsWke","[[\\"test\\",\\"zh-CN\\",\\"zh-CN\\"],2]",null,"generic"]]]'
    }
    # print(body)
    res = requests.post('https://translate.google.com/_/TranslateWebserverUi/data/batchexecute', headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Referer': 'https://translate.google.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }, data=body)
    httpcode = res.status_code
    # redis_client.incr('times')
    # conn = None
    # try:
    #     conn= mysql.connector.connect(**DATABASE)
    #     cur = conn.cursor()
    #     cur.execute('UPDATE alltimes SET times = times + 1')
    #     conn.commit()
    # finally:
    #     if conn:
    #         conn.close()
    # print(res.text)
    json = {
        "code": httpcode,
    }
    return json

@app.route('/_api/ipaddtimes',methods=["POST"])
def ipaddtimes():
    if turnstile.verify():
        # user_ip = get_remote_address()
        user_ip = request.headers['X-Real-Ip']

        # time, reason = getipban(user_ip)
        # if time:
        #     json = {
        #         "code": 403,
        #         "msg": "已被封禁",
        #         "time": time,
        #         "reason": reason
        #     }
        #     return json
        times, addtimes, checked, addtime, lastusetime = getipinfo(user_ip)

        if 1000*addtimes +1000 > times + 1000*5:
            json = {
                "code": 403,
                "msg": "已达增加次数上限"
            }
            return json
        try:
            conn= mysql.connector.connect(**DATABASE)
            cur = conn.cursor(buffered=True)
            cur.execute(f"UPDATE user SET addtimes = COALESCE(addtimes, 0) WHERE ip = '{user_ip}';")
            cur.execute(f"INSERT INTO user (ip, addtimes, addtime) VALUES ('{user_ip}', 1, NOW()) ON DUPLICATE KEY UPDATE addtimes = addtimes + 1, addtime = NOW();")
            conn.commit()
        finally:
            if conn:
                conn.close()

        json = {
            "code": 200,
            "msg": "成功",
            "addtimes": addtimes + 1,
        }
        return json
    else:
        # FAILED
        json = {
            "code": 403,
            "msg": "未通过验证"
        }
        return json

@app.route('/_api/ipcheck',methods=["POST"])
def ipcheck():
    if turnstile.verify():
        # user_ip = get_remote_address()
        user_ip = request.headers['X-Real-Ip']

        # time, reason = getipban(user_ip)
        # if time:
        #     json = {
        #         "code": 403,
        #         "msg": user_ip+"已被封禁",
        #         "time": time,
        #         "reason": reason
        #     }
        #     return json
        times, addtimes, checked, addtime, lastusetime = getipinfo(user_ip)

        if checked == 1:
            json = {
                "code": 403,
                "msg": user_ip+"已经完成过验证",
            }
            return json
        
        try:
            conn= mysql.connector.connect(**DATABASE)
            cur = conn.cursor(buffered=True)
            cur.execute(f"UPDATE user SET checked = COALESCE(checked, 0) WHERE ip = '{user_ip}';")
            cur.execute(f"INSERT INTO user (ip, checked) VALUES ('{user_ip}', 1) ON DUPLICATE KEY UPDATE checked = 1")
            conn.commit()
        finally:
            if conn:
                conn.close()

        json = {
            "code": 200,
            "msg": user_ip+"验证成功",
        }
        return json
    else:
        # FAILED
        json = {
            "code": 403,
            "msg": "未通过验证，请刷新重试"
        }
        return json
@app.route('/_api/ipinfo')
def ipinfo():
    # user_ip = get_remote_address()
    user_ip = request.headers['X-Real-Ip']
    times, addtimes, checked, addtime, lastusetime = getipinfo(user_ip)
    if checked == 1:
        checked_bool = True
    else:
        checked_bool = False
    json = {
        "code": 200,
        "times": times,
        "addtimes": addtimes,
        "checked": checked_bool,
        "addtime": addtime,
        "lastusetime": lastusetime,
        "ip": user_ip
    }
    return json

@app.route('/_api/iphistory')
def iphistory():
    try:
        conn= mysql.connector.connect(**DATABASE)
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT * FROM `gtdata`.`user` WHERE DATE(`lastusetime`) = CURDATE() ORDER BY `lastusetime` DESC LIMIT 0,30;")
        conn.commit()
        result = cur.fetchall()
        history = []
        if result:
            for i in range(len(result)):
                ip = result[i][0]
                region = extra.get_ip_region(ip)
                lastusetime = result[i][5]
                if result[i][1]:
                    times = result[i][1]
                else:
                    times = 0
                perip = {
                    "ip": extra.anonymize_ip(ip),
                    "region": region,
                    "times": times,
                    "lastusetime": lastusetime
                }
                history.append(perip)
    # 出错处理
    except Exception as e:
        json = {
            "code": 503,
            "msg": str(e)
        }
        return json
    finally:
        if conn:
            conn.close()
    json = {
        "code": 200,
        "history": history
    }
    return json

def getipinfo(ip):
    try:
        conn= mysql.connector.connect(**DATABASE)
        cur = conn.cursor(buffered=True)
        cur.execute(f"SELECT * FROM user WHERE ip = '{ip}'")
        conn.commit()
        result = cur.fetchall()
        if result:
            if result[0][1]:
                times = result[0][1]
            else:
                times = 0
            if result[0][2]:
                addtimes = result[0][2]
            else:
                addtimes = 0
            if result[0][3]:
                checked = result[0][3]
            else:
                checked = 0
            addtime = result[0][4]
            lastusetime = result[0][5]
            return times, addtimes, checked, addtime, lastusetime
        else:
            newipdata(ip)
            return 0, 0, 0, '', ''
    finally:
        if conn:
            conn.close()


def newipdata(ip):
    try:
        conn= mysql.connector.connect(**DATABASE)
        cur = conn.cursor(buffered=True)
        cur.execute(f"INSERT INTO user (ip,times,addtimes,checked) VALUES ('{ip}',0,0,0) ON DUPLICATE KEY UPDATE times = 0, addtimes = 0, checked = 0")
        conn.commit()
    finally:
        if conn:
            conn.close()
            
# def getipban(ip):
#     try:
#         conn= mysql.connector.connect(**DATABASE)
#         cur = conn.cursor(buffered=True)
#         cur.execute(f"SELECT * FROM ipban WHERE ip = '{ip}'")
#         conn.commit()
#         result = cur.fetchall()
#         if result:
#             time = result[0][1]
#             reason = result[0][2]
#             return time, reason
#         else:
#             return False, False
#     finally:
#         if conn:
#             conn.close()

def loadcookies():
    # 打开cookies.json
    s = open('cookies.json', 'r', encoding='utf-8').read()
    pat = re.compile(r'(true,)|(false,)|(null,)|(null)')
    r = pat.sub('"a",', s)
    # 将剪切板内容作为字典输入
    cookie_list = eval(r)
    result_list = []

    for dic in cookie_list:
        s = dic.get('name') + '=' + dic.get('value') + ';'
        result_list.append(s)

    result = ''.join(result_list)
    cookies_dict = {cook.split('=')[0]:cook.split('=')[1] for cook in result.split('; ')}
    return cookies_dict

def processcookies(cookies):
    result_list = []

    for name, value in cookies.items():
        s = name + '=' + value + ';'
        result_list.append(s)

    result = ''.join(result_list)
    cookies_dict = {cook.split('=')[0]:cook.split('=')[1] for cook in result.split('; ')}
    return cookies_dict
    
if __name__ == '__main__':
    starttime = datetime.now()
    # timer_thread = threading.Thread(target=run_timer)
    # timer_thread.daemon = True
    # timer_thread.start()
    cookies = loadcookies()
    app.run(debug=True,host='0.0.0.0',port=6010)
    #app.run(debug=False,host='0.0.0.0')