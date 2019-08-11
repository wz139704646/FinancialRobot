# from app.utils.DBHelper import MyHelper
# import os
# import yaml
#
# # 如果表不存在则新建表
# base = os.path.abspath(os.path.dirname(__file__))
# sql_relative = '../static/sql/finance_tbls.sql'
# sql_target = os.path.join(base, sql_relative)
# data_relative = '../static/sql/subjects_original_data.yml'
# data_target = os.path.join(base, data_relative)
# conn = MyHelper()
# conn.executeCreate(filename=sql_target)
#
# # 如果基础数据不存在则插入
# insert_sql = "insert ignore into accounting_subjects(subject_code, name, superior_subject_code, type, type_detail) " \
#              "values (%s, %s, %s, %s, %s)"
# with open(data_target, 'r', encoding='utf-8') as fd:
#     data = yaml.load(fd.read(), Loader=yaml.FullLoader)
#     for tp in data:
#         type = tp.get('type')
#         subs = tp.get('subjects')
#         if type == '损益类':
#             increase_type_detail = '收入类'
#             decrease_type_detail = '费用类'
#             for increase_item in subs.get(increase_type_detail):
#                 conn.executeUpdate(insert_sql, param=[increase_item.get('code'), increase_item.get('name'),
#                                                       increase_item.get('superior_subject_code'), type, increase_type_detail])
#             for decrease_item in subs.get(decrease_type_detail):
#                 conn.executeUpdate(insert_sql, param=[decrease_item.get('code'), decrease_item.get('name'),
#                                                       decrease_item.get('superior_subject_code'), type, decrease_type_detail])
#         else:
#             for item in subs:
#                 conn.executeUpdate(insert_sql, param=[item.get('code'), item.get('name'),
#                                                       item.get('superior_subject_code'), type, None])
