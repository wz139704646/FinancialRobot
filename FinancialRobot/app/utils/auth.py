import functools
from flask import jsonify, request
import logging
import datetime, time
from app import config
import jwt
import json

logger = logging.getLogger(__name__)


def check_token(func):
    """
    装饰器，验证token
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = Auth.identify(request)
        if res['auth']:
            return func(*args, **kwargs)
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
        print(auth_header)
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
