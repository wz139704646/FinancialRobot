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

# 获取当前脚本所在文件夹路径
curPath = os.path.dirname(os.path.realpath(__file__))
# 获取yaml文件路径
yamlPath = os.path.join(curPath, "permission.yml")

# open方法打开直接读出来
f = open(yamlPath, 'r', encoding='utf-8')
cfg = f.read()  # 读出来是字符串

d = yaml.load(cfg, Loader=yaml.FullLoader)  # 用load方法转字典
print(d['features'])
print(type(d))
