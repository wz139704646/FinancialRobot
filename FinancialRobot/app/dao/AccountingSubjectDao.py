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
        :return: dict类型，字段名为 accounting_subjects natural join accounting_subject_balance 产生临时表的字段，
                                加上 credit_debit（余额为借或贷方金额） 以及计算所得的期末余额
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
                    'credit_debit': '借' if cd_dict['credit'] > 0 else '贷',
                    'closing_balance': row[6] + row[7] * cd_dict['credit'] + row[8] * cd_dict['debit']
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

    # 递归查询子科目
    def query_sub_subject(self, subject_code):
        """
        查询某一科目的所有子科目
        :param subject_code: 该科目的科目代码
        :return: list类型，每一个元素是该科目的所有子科目信息的tuple，按字符串方式进行排列，若返回值为空数组，则表明无子科目
        """
        rows = self.query_subject(cond={'superior_subject_code': subject_code})
        res = []
        if rows:
            res.extend(list(rows))
        else:
            return res

        for row in rows:
            res.extend(self.query_sub_subject(row[0]))
        return res

        # return conn.executeQuery(
        #     sql="with recursive subs as "
        #         "(select * from accounting_subjects where superior_subject_code = %s "
        #         "union all "
        #         "select * from accounting_subjects "
        #         "where superior_subject_code in ("
        #         "select subject_code from subs"
        #         ")"
        #         ")select * from subs order by subject_code asc",
        #     param=[subject_code]
        # )

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

        if not all([not data.get('subject_code'), not data.get('name'), not data.get('type'),
                    not data.get('type_detail')]):
            sql = "update accounting_subjects set "
            param = []
            if data.get('subject_code'):
                sql += "subject_code = %s "
                param.append(data.get('subject_code'))
                new_data['subject_code'] = data.get('subject_code')
            if data.get('name'):
                sql += "name = %s "
                param.append(data.get('name'))
                new_data['name'] = data.get('name')
            if data.get('type'):
                sql += "type = %s "
                param.append(data.get('type'))
                new_data['type'] = data.get('type')
            if data.get('type_detail'):
                sql += "type_detail = %s "
                param.append(data.get('type_detail'))
                new_data['type_detail'] = data.get('type_detail')
            sql += "where subject_code = %s"
            param.append(subject_code)
            row = conn.executeUpdate(sql, param)
            if row:
                return True, old_data, new_data
            else:
                return False, '科目信息错误，更新失败'
        else:
            return False, '缺少科目更新后的数据'

    def query_subject_balance(self, cond):
        """
        查询科目余额
        :param cond: dict类型. 字段time——查询某一期的余额，subject_code——查询科目代码指定的特定科目的余额，
                        字段name——查询特定名称科目的余额，字段superior_subject_code——查询特定科目的下级科目的余额
                        字段type——拆线呢特定类别的科目的余额，字段type_detail——查询特定详情类别科目的余额
        :return: list of dict. 字段time——期（时间段），subject_code——科目代码，opening_balance——期初余额，
                            credit——期间借方发生金额，debit——期间贷方发生金额，closing_balance——期末余额
        """
        rows = self.query_subject(cond)
        if rows:
            # 所查询科目存在
            conn = MyHelper()
            cond = cond or {}
            subjects = self.accounting_subject_to_dict(rows)
            res = []
            for subject in subjects:
                rows_sub = self.query_subject({'superior_subject_code': subject.get('subject_code')})
                if rows_sub:
                    # 科目有子科目
                    # 将数额类值均初始化为0
                    subject['opening_balance'] = 0
                    subject['credit'] = 0
                    subject['debit'] = 0
                    subject['closing_balance'] = 0
                    if cond.get('time'):
                        # 限定了期数，则通过递归调用，将所有的子科目余额叠加作为上级科目的科目余额
                        sub_balance = self.query_subject_balance({'time': cond.get('time'),
                                                                  'superior_subject_code': subject.get('subject_code')})
                        if len(sub_balance):
                            subject['time'] = cond.get('time')
                            subject['credit_debit'] = sub_balance[0].get('credit_debit')
                            for bal in sub_balance:
                                subject['opening_balance'] += bal.get('opening_balance')
                                subject['credit'] += bal.get('credit')
                                subject['debit'] += bal.get('debit')
                                subject['closing_balance'] += sub_balance[0].get('closing_balance')
                            res.append(subject)
                    else:
                        # 未限制期数，存在多期，需要复制多份
                        sub_balance = self.query_subject_balance({'superior_subject_code': subject.get('subject_code')})
                        # 时间字典
                        time_dict = {}
                        for bal in sub_balance:
                            subject_time = time_dict.get(bal.get('time'))
                            if subject_time is None:
                                # 复制一份添加到字典中
                                subject_time = subject.copy()
                                time_dict[bal.get('time')] = subject_time
                                subject_time['credit_debit'] = bal.get('credit_debit')
                                subject_time['time'] = bal.get('time')
                            subject_time['opening_balance'] += bal.get('opening_balance')
                            subject_time['credit'] += bal.get('credit')
                            subject_time['debit'] += bal.get('debit')
                            subject_time['closing_balance'] += bal.get('closing_balance')
                        # 将字典的值加入返回数据
                        res.extend(list(time_dict.values()))
                else:
                    # 科目无子科目
                    sql = "select * from accounting_subjects natural join accounting_subjects_balance " \
                          "where subject_code = %s"
                    params = [subject.get('subject_code')]
                    if cond.get('time'):
                        sql += " and time = %s"
                        params.append(cond.get('time'))
                    sql += " order by time desc"
                    res.extend(self.subject_balance_to_dict(list(conn.executeQuery(sql, params) or [])))

            return res

    def query_subject_balance_by_time_range(self, cond, low=None, up=None):
        """
        根据时间范围查询科目余额
        :param cond: 查询科目的限定条件
        :param low: 时间下界（大于等于）
        :param up: 时间上界（小于等于）
        :return: dict类型，同query_subject_balance
        """
        if not low and not up:
            return self.query_subject_balance(cond)
        if low and up and low > up:
            return

        rows = self.query_subject(cond)
        if rows:
            # 所查询科目存在
            conn = MyHelper()
            cond = cond or {}
            subjects = self.accounting_subject_to_dict(rows)
            res = []
            for subject in subjects:
                rows_sub = self.query_subject({'superior_subject_code': subject.get('subject_code')})
                if rows_sub:
                    # 科目有子科目
                    # 将数额类值均初始化为0
                    subject['opening_balance'] = 0
                    subject['credit'] = 0
                    subject['debit'] = 0
                    subject['closing_balance'] = 0

                    sub_balance = self.query_subject_balance_by_time_range({
                        'superior_subject_code': subject.get('subject_code')}, low, up)
                    # 时间字典
                    time_dict = {}
                    for bal in sub_balance:
                        subject_time = time_dict.get(bal.get('time'))
                        if subject_time is None:
                            # 复制一份添加到字典中
                            subject_time = time_dict[bal.get('time')] = subject.copy()
                            subject_time['credit_debit'] = bal.get('credit_debit')
                            subject_time['time'] = bal.get('time')
                        subject_time['opening_balance'] += bal.get('opening_balance')
                        subject_time['credit'] += bal.get('credit')
                        subject_time['debit'] += bal.get('debit')
                        subject_time['closing_balance'] += bal.get('closing_balance')
                    # 将字典的值加入返回数据
                    res.extend(list(time_dict.values()))
                else:
                    # 科目无子科目
                    sql = "select * from accounting_subjects natural join accounting_subjects_balance " \
                          "where subject_code = %s"
                    params = [subject.get('subject_code')]
                    if low:
                        sql += " and time >= %s"
                        params.append(low)
                    if up:
                        sql += " and time <= %s"
                        params.append(up)
                    sql += " order by time desc"
                    res.extend(self.subject_balance_to_dict(list(conn.executeQuery(sql, params) or [])))

            return res

    # 更新科目余额信息，每次更新具有原子性，即其中一项错误则整个更新全部取消
    def update_subject_balance(self, data):
        """
        更新科目余额信息
        :param data: list 类型，每个元素为包含查询条件以及更新的数据的字典，字段组成：
        time *: 期, subject_code *: 科目代码, opening_balance: 期初余额, { way, value }
        credit: 借方金额变动{ way, value }, debit: 贷方金额变动{  way, value }, way: set / update，表示设定或更新
        :return: tuple, 第一个元素表示是否成功，第二个元素是成功时的更新前数据或失败时的信息，第三个元素是新数据
        """
        sqls = []
        params = []
        conn = MyHelper()
        olds = []
        news = []
        for d in data:
            if not all([d.get('time'), d.get('subject_code')]):
                return False, "科目余额更新失败：缺少必要参数：期数和科目代码"
            old = self.query_subject_balance(cond={'subject_code': d.get('subject_code'), 'time': d.get('time')})
            if not len(old):
                return False, "科目({})余额更新失败：查不到该科目余额信息".format(d.get('subject_code'))
            # 原科目余额的期末余额
            closing_delta = 0

            sql_update_cur = "update accounting_subjects_balance set "
            params_cur = []

            credit = d.get('credit')
            debit = d.get('debit')
            opening_balance = d.get('opening_balance')

            # 更新相应字段并重新计算期末余额
            if credit:
                if credit.get('way') == 'set':
                    sql_update_cur += "credit = %s, "
                    params_cur.append(credit.get('value'))
                    if old[0].get('credit_debit') == '借':
                        closing_delta += credit.get('value') - old[0].get('credit')
                    else:
                        closing_delta -= credit.get('value') - old[0].get('credit')
                else:
                    sql_update_cur += "credit = credit + %s, "
                    params_cur.append(credit.get('value'))
                    if old[0].get('credit_debit') == '借':
                        closing_delta += credit.get('value')
                    else:
                        closing_delta -= credit.get('value')

            if debit:
                if debit.get('way') == 'set':
                    sql_update_cur += "debit = %s, "
                    params_cur.append(debit.get('value'))
                    if old[0].get('credit_debit') == '贷':
                        closing_delta += debit.get('value') - old[0].get('debit')
                    else:
                        closing_delta -= debit.get('value') - old[0].get('debit')
                else:
                    sql_update_cur += "debit = debit + %s, "
                    params_cur.append(debit.get('value'))
                    if old[0].get('credit_debit') == '贷':
                        closing_delta += debit.get('value')
                    else:
                        closing_delta -= debit.get('value')

            if opening_balance:
                if opening_balance.get('way') == 'set':
                    sql_update_cur += "opening_balance = %s, "
                    params_cur.append(opening_balance.get('value'))
                    closing_delta += opening_balance.get('value') - old[0].get('opening_balance')
                else:
                    sql_update_cur += "opening_balance = opening_balance + %s, "
                    params_cur.append(opening_balance.get('value'))
                    closing_delta += opening_balance.get('value')

            sql_update_cur += "time = time where time = %s and subject_code = %s"
            params_cur.append(d.get('time'))
            params_cur.append(d.get('subject_code'))
            olds.append(old[0])

            # 用于更新当前期之后所有期的期初余额的sql语句
            sql_update_later = "update accounting_subjects_balance set opening_balance = opening_balance + %s " \
                               "where subject_code = %s and time > %s"
            param_later = [closing_delta, d.get('subject_code'), d.get('time')]

            sqls.extend([sql_update_cur, sql_update_later])
            params.extend([params_cur, param_later])

        rows = conn.executeUpdateTransaction(sqls=sqls, params=params)
        if rows:
            for bal in olds:
                news.extend(self.query_subject_balance({
                    'subject_code': bal.get('subject_code'),
                    'time': bal.get('time')
                }))
            return True, olds, news
        else:
            return False, '科目余额更新失败：信息有误'

    # 插入之前的科目余额时需要更新之后的科目余额
    def insert_subject_balance(self, data):
        """
        插入科目余额记录
        :param data: dict类型，time subject_code必填, opening_balance credit debit选填
        opening_balance不填默认为上一期期末余额或0, credit debit 不填默认0
        :return: tuple类型，第一个元素为是否插入成功，第二个元素为错误时的错误信息或成功时插入的数据
        """
        if not all([data.get('time'), data.get('subject_code')]):
            return False, "科目余额添加失败：缺少必要参数：期数和科目代码"

        conn = MyHelper()
        sql = "insert into accounting_subjects_balance(time, subject_code, opening_balance, credit, debit) " \
              "values(%s, %s, %s, %s, %s)"
        params = []
        if data.get('opening_balance') is None:
            last = int(data.get('time')) - 1
            if last % 100 == 0:
                last = last - 100 + 12
            last_balance = self.query_subject_balance_by_time_range({
                'subject_code': data.get('subject_code')}, up=str(last))
            if not len(last_balance):
                # 不存在前一期的科目余额
                data['opening_balance'] = 0
            else:
                # 将期初余额设置为前一期的期末余额
                last_balance = last_balance[0]
                data['opening_balance'] = last_balance.get('closing_balance')
        params.append(data.get('time'))
        params.append(data.get('subject_code'))
        params.append(data.get('opening_balance'))
        params.append(data.get('credit') or 0)
        params.append(data.get('debit') or 0)

        rows = conn.executeUpdate(sql, params)
        if rows:
            new_data = self.query_subject_balance({'time': data.get('time'), 'subject_code': data.get('subject_code')})[0]
            # 更新该期之后每一期的期初余额
            conn.executeUpdate(
                sql="update accounting_subjects_balance "
                    "set opening_balance = opening_balance + %s "
                    "where subject_code = %s and time > %s",
                param=[new_data.get('closing_balance')-new_data.get('opening_balance'),
                       data.get('subject_code'), data.get('time')]
            )
            return True, new_data
        else:
            return False, '科目余额添加失败：信息有误'

    # 根据条件删除科目余额信息
    def delete_subject_balance(self, cond={}):
        """
        删除科目余额信息（一般用于删除为空的科目余额信息）
        :param cond: dict类型，作为删除余额信息的查询条件，可选字段有——
        time: 科目期数
        subject_code: 科目代码
        :return: tuple类型，第一个元素为操作是否成功，第二个参数为所删除的数据
        """
        cond = cond or {}
        bals = self.query_subject_balance(cond)
        conn = MyHelper()
        if len(bals):
            sql = "delete from accounting_subjects_balance where 1=1"
            param = []
            if cond.get('time'):
                sql += " and time = %s"
                param.append(cond.get('time'))
            if cond.get('subject_code'):
                sql += " and subject_code = %s"
                param.append(cond.get('subject_code'))
            rows = conn.executeUpdate(sql, param)
            if rows:
                return True, bals
            else:
                return False, '删除科目余额信息失败'
        else:
            return False, '找不到相关科目余额信息'

    # 查询最上一层的科目代码
    def query_top_subject(self, subject_code):
        subject = self.query_subject({'subject_code': subject_code})
        if subject:
            subject = self.accounting_subject_to_dict(subject)[0]
            if subject.get('superior_subject_code'):
                return self.query_top_subject(subject.get('superior_subject_code'))
            else:
                return subject

