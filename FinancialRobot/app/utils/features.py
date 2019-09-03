# coding:utf-8
import yaml
import os


def get_permission():
    # 获取当前脚本所在文件夹路径
    cur_path = os.path.dirname(os.path.realpath(__file__))
    # 获取yaml文件路径
    yaml_path = os.path.join(cur_path, "../permission.yml")
    # open方法打开直接读出来
    file = open(yaml_path, 'r', encoding='utf-8')
    # 用load方法转字典
    _permission = yaml.load(file.read(), Loader=yaml.FullLoader)
    file.close()
    # print(permission['features'])
    # print(permission['roles'])
    return _permission


def get_roles():
    _all = get_permission()
    # print(_all['roles'])
    names = []
    for role in _all['roles']:
        names.append(role['name'])
    return names

def get_features():
    _all = get_permission()
    # print(_all['roles'])
    names = []
    for feature in _all['features']:
        names.append(feature['name'])
    return names


