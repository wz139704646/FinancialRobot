#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class AccountingSubjectDao:
    # 对不同类别以及详细类别的科目的借贷所代表的增加还是减少字典
    rate_for_subjects_of_types = {
        '资产类': {'credit': 1, 'debit': -1},
        '负债类': {'credit': -1, 'debit': 1},
        '权益类': {'credit': -1, 'debit': 1},
        '损益类': {'收入类': {'credit': -1, 'debit': 1},
                '费用类': {'credit': 1, 'debit': -1}},
        '成本类': {'credit': 1, 'debit': -1}
    }

    @classmethod
    def accounting_subject_to_dict(cls, data):
        result = []
        for row in data:
            result.append({
                'subject_code': row[0],
                'name': row[1],
                'superior_subject_code': row[2],
                'type': row[3]
            })
        return result

    def query_subject(self, cond={}):
        """
        查询科目信息，使用条件严格查询
        :param cond: 字典类型，为查询条件, 与返回值字段组成相同，每个字段均可为空
        :return: tuple类型，字段名按accounting_subject表的构成排列
        """
        conn = MyHelper()
        params = []

        sql = "select * from accounting_subjects where 1 = 1"
        if cond.get('subject_code'):
            sql += " and subject_code = %s"
            params.append(cond.get('subject_code'))
        if cond.get('name'):
            sql += " and name = %s"
            params.append(cond.get('name'))
        if cond.get('superior_subject_code'):
            sql += " and superior_subject_code = %s"
            params.append(cond.get('superior_subject_code'))
        if cond.get('type'):
            sql += " and type = %s"
            params.append(cond.get('type'))
        if cond.get('type_detail'):
            sql += " and type_detail = %s"
            params.append(cond.get('type_detail'))

        sql += ' order by subject_code asc'
        return conn.executeQuery(sql=sql, param=params)

    def query_subject_type_rate(self, subject_code):
        """
        查询科目的类别和其借贷对应为增长或减少
        :param subject_code: 科目代码
        :return: {
            'type': 科目种类,
            'credit': 科目借代表的增加或减少
            'debit': 科目贷代表的增加或减少
        }
        """
        conn = MyHelper()
        rows = conn.executeQuery(
            sql="select type, type_detail from accounting_subjects "
                "where subject_code = %s",
            param=[subject_code]
        )
        if len(rows):
            type = rows[0][0]
            type_detail = rows[0][1]
            rate = AccountingSubjectDao.rate_for_subjects_of_types.get(type)
            if all([rate, rate.get(type_detail)]):
                result = {'type': type, 'rate': rate.get(type_detail)}
            elif rate:
                result = {'type': type, 'rate': rate}
            return result

    def insert_detail_subject(self, data):
        """
        新增明细科目
        :param data: 字典类型，明细科目的必需数据——subject_code, name, superior_subject_code
        :return: True, ——插入成功
                False, errMsg——插入失败，错误信息
        """
        conn = MyHelper()
        if not all([data.get('subject_code'), data.get('name'), data.get('superior_subject_code')]):
            return False, '科目信息不完整'

        # 根据上级科目的科目代码获取该明细科目的类别和具体类别
        subject = self.query_subject({'subject_code': data.get('superior_subject_code')})
        if subject and len(subject):
            subject_dict = self.accounting_subject_to_dict(subject[:1])[0]
            data['type'] = subject_dict.get('type')
            data['type_detail'] = subject_dict.get('type_detail')

            if conn.executeUpdate(
                sql="insert into accounting_subjects(subject_code, name, superior_subject_code, type, type_detail)"
                    " values(%s, %s, %s, %s, %s)",
                param=[data.get('subject_code'), data.get('name'), data.get('superior_subject_code'), data.get('type'), data.get('type_detail')]
            ):
                return True
            else:
                return False, '科目代码重复或信息不正确'
        else:
            return False, '上级科目不存在'

    def query_sub_subject(self, subject_code):
        """
        查询某一科目的所有子科目
        :param subject_code: 该科目的科目代码
        :return: tuple类型，该科目的所有子科目，按字符串方式进行排列
        """
        conn = MyHelper()
        return conn.executeQuery(
            sql="with recursive subs as "
                "(select * from accounting_subjects where superior_subject_code = %s "
                "union all "
                "select * from accounting_subjects "
                "where superior_subject_code in ("
                "select subject_code from subs"
                ")"
                ")select * from subs order by subject_code asc",
            param=[subject_code]
        )

    def query_lv_one_sub_subject(self, subject_code):
        """
        查询某一科目的所有一级子科目
        :param subject_code: 该科目的科目代码
        :return: str类型，可能为空，空则代表无子科目
        """
        conn = MyHelper()
        return conn.executeQuery(
            sql="select * from accounting_subjects "
                "where superior_subject_code = %s",
            param=[subject_code]
        )

    def query_all_types(self):
        """
        查询所有科目类别
        :return: list类型，包含所有类别（字符串）
        """
        conn = MyHelper()
        rows =  conn.executeQuery(
            "select type from accounting_subjects "
            "group by type"
        )
        if rows:
            result = []
            for row in rows:
                result.append(row[0])
            return result
