from app.utils.util import decode_jwt
from flask import Flask,render_template,redirect,request,session
import logging
import functools
logger = logging.getLogger(__name__)


def check_token(func):
    """
    装饰器，验证token
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(request)
        token = request.headers.get("Authorization")
        print(token)
        if token:
            try:
                # 验证token
                payload = decode_jwt(token)
            except:
                logger.info("Wrong oken: {token}".format(token=token))
                raise Exception('请求被拒绝')
            else:
                # token正确，将用户信息存入request.META["REMOTE_USER"]
                args[1].headers["REMOTE_USER"] = payload['data']
                return func(*args, **kwargs)
        else:
            logger.info("Without token! {request}".format(request=args[1].headers))
            raise Exception('没有携带token')

    return wrapper


'''
def check_team_token(func):
    """
    装饰器，验证team_token
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        # TODO: 注意，这里粗略的获取了request对象，目前该装饰器只能装饰request在函数的第二个参数的函数
        token = args[1].META.get("HTTP_TOKEN")
        if token:
            try:
                info = decode_jwt(token) #验证token
            except:
                logger.info("Wrong oken: {token}".format(token=token))
                raise NotLogin
            else:
                # token正确，将用户信息存入request.META["REMOTE_USER"]
                if info.get("type") == "team":
                    args[1].META["REMOTE_USER"] = info
                    return func(*args, **kwargs)
                else:
                    raise PermissionDeny
        else:
            logger.info("Without token! {request}".format(request=args[1].META))
            raise NotLogin

    return wrapper


def check_referee_token(func):
    """
    装饰器，验证referee_token
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        # TODO: 注意，这里粗略的获取了request对象，目前该装饰器只能装饰request在函数的第二个参数的函数
        token = args[1].META.get("HTTP_TOKEN")
        if token:
            try:
                info = decode_jwt(token) #验证token
            except:
                logger.info("Wrong oken: {token}".format(token=token))
                raise NotLogin
            else:
                # token正确，将用户信息存入request.META["REMOTE_USER"]
                if info.get("type") == "referee":
                    args[1].META["REMOTE_USER"] = info
                    return func(*args, **kwargs)
                else:
                    raise PermissionDeny
        else:
            logger.info("Without token! {request}".format(request=args[1].META))
            raise NotLogin

    return wrapper

'''