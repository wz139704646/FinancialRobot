import json


def return_success(data):
    res = {'success': True, 'result': data}
    return res


def return_unsuccess(err_msg):
    res = {'success': False, 'errMsg': err_msg}
    return res
