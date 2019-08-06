# class Features:
#     name = ''
#     allow_api = []
#
#     @classmethod
#     def get_subclass(cls):
#         return cls.__subclasses__()
#
#
# class FinancialProcessing(Features):
#     name = 'financial_processing'
#     allow_api = ['123']
#
#
# for f in Features.get_subclass():
#     print(getattr(f, 'name'))

# coding:utf-8
import yaml
import os


def get_permission():
    # 获取当前脚本所在文件夹路径
    cur_path = os.path.dirname(os.path.realpath(__file__))
    # 获取yaml文件路径
    yaml_path = os.path.join(cur_path, "permission.yml")
    # open方法打开直接读出来
    file = open(yaml_path, 'r', encoding='utf-8')
    # 用load方法转字典
    permission = yaml.load(file.read(), Loader=yaml.FullLoader)
    print(permission['features'])
    print(permission['roles'])
    return permission


get_permission()
