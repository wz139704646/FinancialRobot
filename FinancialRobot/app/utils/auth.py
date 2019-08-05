from flask import jsonify, request
import logging
import datetime, time
from app import config
import jwt
from app.dao.UserDao import UserDao
from app.features import get_permission
from app.utils.json_util import *

logger = logging.getLogger(__name__)


# 检查权限
def check_permission(account):
    pre_endpoint = str(request.endpoint)
    pre_feature = UserDao().query_permission(account)
    allow_feature = get_permission()
    flag = False
    for feature in allow_feature['features']:
        if pre_feature is feature['name'] and pre_endpoint in feature['api']:
            flag = True
    return flag


def check_token(func):
    """
    装饰器，验证token
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        res = Auth.identify(request)
        if res.get('auth'):
            data = res.get('data')
            account = data.get('data').get('account')
            try:
                if check_permission(account):
                    return func(*args, **kwargs)
                else:
                    return json.dumps(return_unsuccess('Permission Denied'))
            except Exception as e:
                return json.dumps((return_unsuccess("Error: " + str(e))))
        else:
            # raise Exception(res['errMsg'])
            return json.dumps(res, ensure_ascii=False), 555

    return wrapper


class Auth:
    @staticmethod
    def create_jwt(user_dict):
        """
        生成token
        :param user_dict:  用户信息字典
        :return:  token 字符串
        """

        # 封装token加密前内容
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(days=60)
        payload = {
            'exp': expire_time,
            'iat': datetime.datetime.utcnow(),
            'data': user_dict
        }
        encoded = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
        token = str(encoded, encoding='ascii')
        return token

    @staticmethod
    def decode_jwt(token):
        """
        解密token
        :param token:  token 字符串
        :return:  包含用户信息字典的payload
        """
        payload = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
        if 'data' in payload and 'exp':
            data = payload['data']
            return payload
        else:
            raise jwt.InvalidTokenError

    @staticmethod
    def identify(_request):
        """
        用户鉴权
        :param _request: 发起的请求
        :return: 验证结果，{
                                'auth': 是否成功
                                'errMsg': 调用是否成功的提示信息
                                'data': 如果成功时返回，用户信息字典
                            }
        """
        auth_header = _request.headers.get('Authorization')
        if auth_header:
            # 请求头中携带Authorization格式为：JWT jwtstr
            token_arr = auth_header.split(' ')
            if (not token_arr) or (token_arr[0] != "JWT") or (len(token_arr) != 2):
                return {'auth': False, 'errMsg': '验证头信息不正确'}
            else:
                auth_token = token_arr[1]
                try:
                    payload = Auth.decode_jwt(auth_token)
                except Exception as e:
                    print(e)
                    return {'auth': False, 'errMsg': 'token解码失败'}
                else:
                    return {'auth': True, 'data': payload, 'errMsg': 'token解码成功'}
        else:
            return {'auth': False, 'errMsg': '没有携带token'}
