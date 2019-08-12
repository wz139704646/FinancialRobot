#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class GeneralVoucherDao:
    @classmethod
    def general_voucher_to_dict(cls, data):
        """
        将general_voucher表中查询出的全部结果转为字典数组
        :param data: 查询到的结果
        :return: 数组类型，每一个元素是表中一行转为字典后的结果
        """
        result = []
        for row in data:
            result.append({
                'date': row[0],
                'record_date': row[1],
                'voucher_no': row[2],
                'attachments_number': row[3],
                'checked': row[4]
            })
        return result

    @classmethod
    def voucher_entry_to_dict(cls, data):
        """
        将voucher_entry表中查询出的全部结果转为字典数组
        :param data: 查询到的结果
        :return: 数组类型，每一个元素是表中一行转为字典后的结果
        """
        result = []
        for row in data:
            result.append({
                'voucher_no': row[0],
                'abstract': row[1],
                'subject_code': row[2],
                'credit_debit': row[3],
                'total': row[4]
            })
        return result

    def insert_voucher(self, data):
        """
        插入新的凭证，包括其各个分录
        :param data: 字典类型，date: 凭证日期，voucher_no：凭证编号, attachments_no：凭证附件数, entries: 凭证分录数组
        entries每一个元素仍为字典, abstract: 分录摘要, subject_code: 分录科目代码, credit_debit：分录金额为"借"/"贷"
                                    total: 分录总金额
        :return: tuple类型, 第一个元素表示是否插入成功, 若成功第二个元素则返回所有数据, 否则第二个元素返回错误信息
        """
        conn = MyHelper()
        if not all([data.get('date'), data.get('voucher_no'), data.get('attachments_no'), data.get('entries')]) \
                and len(data.get('entries')) == 0:
            return False, '凭证信息不全'

        sqls = ["insert into general_voucher (date, voucher_no, attachments_number) "
                "values (%s, %s, %s)"]
        params = [[data.get('date'), data.get('voucher_no'), data.get('attachments_no')]]

        for entry in data.get('entries'):
            if not all([entry.get('abstract'), entry.get('subject_code'), entry.get('credit_debit'), entry.get('total')]):
                return False, '分录信息不全'
            sqls.append("insert into voucher_entry (voucher_no, abstract, subject_code, credit_debit, total) "
                        "values (%s, %s, %s, %s, %s)")
            params.append([data.get("voucher_no"), entry.get('abstract'), entry.get('subject_code'),
                           entry.get('credit_debit'), entry.get('total')])

        rows = conn.executeUpdateTransaction(sqls=sqls, params=params)
        if rows:
            return True, data
        else:
            return False, '凭证或分录信息有误'

    def query_voucher(self, cond={}):
        """
        查询凭证信息（仅限于general_voucher表中信息，不包含凭证）
        :param cond: 查询条件，可以放入任意general_voucher表中已有的字段
        :return: tuple，返回地查询结果
        """
        conn = MyHelper()
        params = []

        sql = "select * from general_voucher where 1 = 1"
        if cond.get('date'):
            sql += " and date = %s"
            params.append(cond.get('date'))
        if cond.get('record_date'):
            sql += " and record_date = %s"
            params.append(cond.get('record_date'))
        if cond.get('voucher_no'):
            sql += " and voucher_no = %s"
            params.append(cond.get('voucher_no'))
        if cond.get('attachments_number'):
            sql += " and attachments_number = %s"
            params.append(cond.get('attachments_number'))
        if cond.get('checked'):
            sql += " and checked = %s"
            params.append(cond.get('checked'))

        sql += ' order by voucher_no asc'
        return conn.executeQuery(sql=sql, param=params)

    def query_voucher_entries(self, voucher_no):
        """
        查询凭证的分录信息
        :param voucher_no: 凭证编号
        :return: tuple类型, 查询voucher_entry表中直接返回的结果
        """
        conn = MyHelper()
        return conn.executeQuery(
            sql="select * from voucher_entry "
                "where voucher_no = %s "
                "order by subject_code",
            param=[voucher_no]
        )

    def update_voucher(self, data):
        """
        更新凭证信息
        :param data: 同insert_voucher的参数
        :return: tuple类型，第一个元素表示是否插入成功，若成功，则第二、第三个元素分别代表更新后的信息和更新前的信息
                                                        否则，第二个元素返回出错信息
        """
        pass