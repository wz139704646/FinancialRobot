#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class GeneralVoucherDao:
    @classmethod
    def general_voucher_to_dict(cls, data):
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

    