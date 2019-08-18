#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class SubjectBalanceDao:
    @classmethod
    def subject_balance_to_dict(cls, data):
        """
        将accounting_subject_balance中查询的结果转换为字典类型
        :param data:
        :return:
        """
        result = []
        for row in data:
            result.append({
                'time': row[0],
                'subject_code': row[1],
                'opening_balance': row[2],
                'credit': row[3],
                'debit': row[4]
            })
        return result