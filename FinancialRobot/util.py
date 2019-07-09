import jwt
import time
# from database_project import settings
#
secret = 'sdagdfdsderedddddddddddddd'
expire_time = int(time.time() + 4*60*60)

def create_jwt(user_dict):
    """
    生成taoke_token
    :param user_dict:  用户信息字典
    :return:  taoke_token 字符串
    """
    encoded = jwt.encode(user_dict, secret, algorithm='HS256')
    taoke_token = str(encoded, encoding='ascii')
    return taoke_token

def decode_jwt(taoke_token):
    """
    解密token
    :param taoke_token:  taoke_token 字符串
    :return:  用户信息字典
    """
    info = jwt.decode(taoke_token, secret, algorithm='HS256')
    return info
