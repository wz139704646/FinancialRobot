from flask import jsonify
import datetime, time
from app import config
import jwt


class Auth():
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
        :return:  用户信息字典
        """
        payload = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
        if 'data' in payload:
            return payload
        else:
            raise jwt.InvalidTokenError

    def identify(self, request):
        """
        用户鉴权
        :param request: 发起的请求
        :return:
        """
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header:
            # 请求头中携带Authorization格式为：JWT jwtstr
            token_arr = auth_header.split(' ')
            if (not token_arr) or (token_arr[0] != "JWT") or (len(token_arr) != 2):
                return {'auth': False, 'errMsg': '验证头信息不正确'}
            else:
                auth_token = token_arr[1]
                try:
                    payload = Auth.decode_jwt(auth_header)
                except Exception as e:
                    print(e)
                    return {'auth': False, 'errMsg': 'token解码失败'}
                else:
                    return {'auth': True, 'data': payload}
        else:
            return {'auth': False, 'errMsg': '没有携带token'}
