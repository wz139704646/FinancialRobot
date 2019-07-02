import json
import random
import re
import threading
import builtins

from flask import Blueprint, request, session
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

sms = Blueprint("sms", __name__)
due = 60 * 5
sms.secret_key = 'sms service 134578631325'

# lock = threading.Lock()
builtins.globals()['verify_code_lock'] = lock = threading.Lock()


@sms.route('/sendSMS', methods=["POST"])
def sendSMS():
    json_data = request.json
    # 腾讯云SMS应用 APPID
    appid = 1400226777
    # 腾讯云SMS应用 APPKEY
    appkey = '8e4b05566cb1021da046f438b5db2736'
    template_id = 111
    sms_sign = 'Fbot'
    phone = json_data.get('phone')
    type = json_data.get('type')

    if not all([phone, type]):
        return json.dumps({"success": False, "errMsg": '参数不全'})

    if not re.match("^1[3578][0-9]{9}$", phone):
        return json.dumps({"success": False, "errMsg": "手机号不正确"})

    ssender = SmsSingleSender(appid, appkey)

    usage = {0: '登录', 1: '注册'}
    code = ''
    for i in range(6):
        code.join(random.randint(0, 9))
    print("verification code:" + code)

    global timer
    timer.cancel()
    timer = threading.Timer(due, timed_rm_verify_code)
    lock.acquire()
    session["verify_code"] = code
    lock.release()
    params = [usage[type], code, round(due / 60)]

    try:
        result = ssender.send_with_param(86, phone, template_id, params, sign=sms_sign, extend="", ext="")
        timer.start()
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    print(result)
    pass


def timed_rm_verify_code():
    lock.acquire()
    if session.get('verify_code') is not None:
        session.pop('verify_code')
    lock.release()


timer = threading.Timer(due, timed_rm_verify_code)
# def get_timer():
#     global timer
#     if timer.is_alive():
#         return timer
#     else:
#         timer = threading.Timer(due, timed_rm_verify_code())
#         timer.
