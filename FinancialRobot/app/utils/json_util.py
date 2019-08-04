import datetime
import decimal
import json


def return_success(data):
    res = {'success': True, 'result': data}
    return res


def return_unsuccess(err_msg):
    res = {'success': False, 'errMsg': err_msg}
    return res


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        super(DecimalEncoder, self).default(o)
