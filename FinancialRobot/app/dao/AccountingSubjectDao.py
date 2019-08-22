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
                'type': row[3],
                'type_detail': row[4]
            })
        return result

    @classmethod
    def subject_balance_to_dict(cls, data):
        """
        将accounting_subjects natural join accounting_subject_balance中查询的结果转换为字典类型
        :param data: 查询accounting_subjects natural join accounting_subject_balance产生的元组
        :return: dict类型，字段名为 accounting_subjects natural join accounting_subject_balance 产生临时表的字段
        """
        result = []
        rate_dict = AccountingSubjectDao.rate_for_subjects_of_types
        for row in data:
            stype = row[3]
            stype_detail = row[4]
            if stype:
                cd_dict = rate_dict[stype]
                if stype_detail and not cd_dict.get('credit'):
                    cd_dict = cd_dict[stype_detail]
                result.append({
                    'subject_code': row[0],
                    'name': row[1],
                    'superior_subject_code': row[2],
                    'type': row[3],
                    'type_detail': row[4],
                    'time': row[5],
                    'opening_balance': row[6],
                    'credit': row[7],
                    'debit': row[8],
                    'closing_balance': row[2] + row[3] * cd_dict['credit'] + row[4] * cd_dict['debit']
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
        cond = cond or {}
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
            _type = rows[0][0]
            type_detail = rows[0][1]
            rate = AccountingSubjectDao.rate_for_subjects_of_types.get(_type)
            if all([rate, rate.get(type_detail)]):
                result = {'type': _type, 'rate': rate.get(type_detail)}
            elif rate:
                result = {'type': _type, 'rate': rate}
            return result

    def insert_subject(self, data):
        """
        新增明细科目
        :param data: 字典类型，明细科目的必需数据——subject_code, name,
        superior_subject_code, type（最后两个其中一个可为空），type_detail（可无）
        :return: True, ——插入成功
                False, errMsg——插入失败，错误信息
        """
        conn = MyHelper()
        if not all([data.get('subject_code'), data.get('name'), data.get('superior_subject_code')])\
                and not all([data.get('subject_code'), data.get('name'), data.get('type')]):
            return False, '科目信息不完整'

        if data.get('superior_subject_code'):
            # 若新增明细科目
            # 根据上级科目的科目代码获取该明细科目的类别和具体类别
            subject = self.query_subject({'subject_code': data.get('superior_subject_code')})
            if subject and len(subject):
                subject_dict = self.accounting_subject_to_dict(subject[:1])[0]
                data['type'] = subject_dict.get('type')
                data['type_detail'] = subject_dict.get('type_detail')
            else:
                return False, '上级科目不存在'

        if conn.executeUpdate(
                sql="insert into accounting_subjects(subject_code, name, superior_subject_code, type, type_detail)"
                    " values(%s, %s, %s, %s, %s)",
                param=[data.get('subject_code'), data.get('name'), data.get('superior_subject_code'), data.get('type'),
                       data.get('type_detail')]
        ):
            return True, data
        else:
            return False, '科目代码重复或其他信息不正确'

    # TODO 递归查询有问题，不确定是否为mysql版本原因
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

    # def query_lv_one_sub_subject(self, subject_code):
    #     """
    #     查询某一科目的所有一级子科目
    #     :param subject_code: 该科目的科目代码
    #     :return: str类型，可能为空，空则代表无子科目
    #     """
    #     conn = MyHelper()
    #     return conn.executeQuery(
    #         sql="select * from accounting_subjects "
    #             "where superior_subject_code = %s "
    #             "order by subject_code asc",
    #         param=[subject_code]
    #     )

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

    def delete_subject(self, subject_code):
        """
        删除科目
        :param subject_code: 索要删除科目的科目代码
        :return: tuple类型，第一个结果返回是否删除成功。成功时第二个返回所删除的科目信息；失败时返回错误信息
        """
        row = self.query_subject({'subject_code': subject_code})
        if row:
            conn = MyHelper()
            res = conn.executeUpdate(
                sql="delete from accounting_subjects where subject_code = %s",
                param=[subject_code]
            )
            if res:
                return True, row
            else:
                return False, '科目已有明细科目，不能直接删除'
        else:
            return False, '找不到该科目'

    def update_subject(self, subject_code, data):
        """
        更新科目信息
        :param subject_code: 所更新的科目的科目代码
        :param data: 用于更新的新数据，字段同accounting_subjects的字段（除superior_subject_code），均为选填
        :return: tuple类型，第一个返回值为是否更新成功。若成功，则第二、三个返回值分别为更新前的数据和更新后的数据；
                                                        若失败，第二个返回值返回错误信息
        """
        if not subject_code:
            return "缺少科目代码参数"
        conn = MyHelper()
        subject = self.query_subject({'subject_code': subject_code})
        if not subject:
            return False, "科目代码出错，找不到该科目"
        old_data = self.accounting_subject_to_dict(subject)[0]
        new_data = old_data.copy()

        if not all([data.get('subject_code') is None, data.get('name') is None, data.get('type') is None,
                    data.get('type_detail') is None]):
            sql = "update accounting_subjects set "
            param = []
            if data.get('subject_code') is not None:
                sql += "subject_code = %s "
                param.append(data.get('subject_code'))
                new_data['subject_code'] = data.get('subject_code')
            if data.get('name') is not None:
                sql += "name = %s "
                param.append(data.get('name'))
                new_data['name'] = data.get('name')
            if data.get('type') is not None:
                sql += "type = %s "
                param.append(data.get('type'))
                new_data['type'] = data.get('type')
            if data.get('type_detail') is not None:
                sql += "type_detail = %s "
                param.append(data.get('type_detail'))
                new_data['type_detail'] = data.get('type_detail')
            sql += "where subject_code = %s"
            param.append(subject_code)
            row = conn.executeUpdate(sql, param)
            if row:
                return True, old_data, new_data
            else:
                return False,'科目信息错误，更新失败'
        else:
            return False, '缺少科目更新后的数据'

    def query_subject_balance(self, cond):
        """
        查询科目余额
        :param cond: dict类型. 字段time——查询某一期的余额，subject_code——查询科目代码指定的特定科目的余额
        :return: dict类型. 字段time——期（时间段），subject_code——科目代码，opening_balance——期初余额，
                            credit——期间借方发生金额，debit——期间贷方发生金额，closing_balance——期末余额
        """
        conn = MyHelper()
        cond = cond or {}
        sql = "select * from accounting_subjects natural join accounting_subjects_balance where 1 = 1"
        params = []
        if cond.get('time'):
            sql += " and time = %s"
            params.append(cond.get('time'))
        if cond.get('subject_code'):
            sql += " and subject_code = %s"
            params.append(cond.get('subject_code'))

        return conn.executeQuery(sql, params)

    def update_subject_balance(self, data):
        """
        更新科目余额信息
        :param data: 查询条件以及更新的数据，字段组成：
        time: 期, subject_code: 科目代码, opening_balance: 期初余额,
        credit: 借方金额变动{ way, value }, debit: 贷方金额变动{  way, value }, way: set / update，表示设定或更新
        :return: tuple, 第一个元素表示是否成功，第二个元素是成功时的更新前数据或失败时的信息，第三个元素是新数据
        """
        if not all([data.get('time'), data.get('subject_code')]):
            return False, "缺少必要参数：期数和科目代码"
        conn = MyHelper()
        old = self.query_subject_balance(cond={'subject_code': data.get('subject_code'), 'time': data.get('time')})
        if not old:
            return False, "找不到该科目余额信息"
        old_data = self.subject_balance_to_dict(old)[0]
        sql = "update accounting_subjects_balance set "
        params = []

        credit = data.get('credit')
        debit = data.debit('debit')
        if credit:
            if credit.get('way') == 'set':
                sql += "credit = %s, "
                params.append(credit.get('value'))
            elif credit.get('value') > 0:
                sql += "credit = credit + %s, "
                params.append(abs(credit.get('value')))
            else:
                sql += "credit = credit - %s, "
                params.append(abs(credit.get('value')))
        if debit:
            if debit.get('way') == 'set':
                sql += "debit = %s, "
                params.append(debit.get('value'))
            elif debit.get('value') > 0:
                sql += "debit = debit + %s, "
                params.append(abs(debit.get('value')))
            else:
                sql += "debit = debit - %s, "
                params.append(abs(debit.get('value')))

        sql += "time = time where time = %s and subject_code = %s"
        params.append(data.get('time'))
        params.append(data.get('subject_code'))

        rows = conn.executeUpdate(sql, params)
        if rows:
            new_data = self.subject_balance_to_dict(self.query_subject_balance(
                cond={'subject_code': data.get('subject_code'), 'time': data.get('time')}))[0]
            return True, old_data, new_data
        else:
            return False, '信息出错或重复，更新无效'

    def insert_subject_balance(self, data):
        """
        插入科目余额记录
        :param data: dict类型，time subject_code必填, opening_balance credit debit选填
        opening_balance不填默认为上一期期末余额或0, credit debit 不填默认0
        :return:
        """
        if not all([data.get('time'), data.get('subject_code')]):
            return False, "缺少必要参数：期数和科目代码"

        conn = MyHelper()
        sql = "insert into accounting_subjects_balance(time, subject_code, opening_balance, credit, debit) " \
              "values(%s, %s, %s, %s, %s)"
        params = []
        if data.get('opening_balance') is None:
            last = int(data.get('time')) - 1
            if last % 100 == 0:
                last = last - 100 + 12
            last_balance = self.query_subject_balance({'time': str(last)})
            if not last_balance:
                data['opening_balance'] = 0
            else:
                last_balance = self.subject_balance_to_dict(last_balance)[0]
                data['opening_balance'] = last_balance.get('closing_balance')
        params.append(data.get('time'))
        params.append(data.get('subject_code'))
        params.append(data.get('opening_balance'))
        params.append(data.get('credit') or 0)
        params.append(data.get('debit') or 0)

        rows = conn.executeUpdate(sql, params)
        if rows:
            return True, self.query_subject_balance({'time': data.get('time'), 'subject_code': data.get('subject_code')})