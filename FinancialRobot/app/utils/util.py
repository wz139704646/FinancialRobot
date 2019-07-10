import jwt, time, datetime
# from database_project import settings
#
from app.config import SECRET_KEY as secret


def create_jwt(user_dict):
    """
    生成token
    :param user_dict:  用户信息字典
    :return:  token 字符串
    """

    # 封装token加密前内容
    expire_time = datetime.datetime.utcnow()+datetime.timedelta(days=60)
    payload = {
        'exp': expire_time,
        'iat': datetime.datetime.utcnow(),
        'data': user_dict
    }
    encoded = jwt.encode(payload, secret, algorithm='HS256')
    token = str(encoded, encoding='ascii')
    return token


def decode_jwt(token):
    """
    解密token
    :param token:  token 字符串
    :return:  用户信息字典
    """
    payload = jwt.decode(token, secret, algorithm='HS256')
    if 'data' in payload:
        return payload
    else:
        raise jwt.InvalidTokenError
