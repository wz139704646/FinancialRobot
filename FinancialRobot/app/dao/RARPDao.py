from app.utils.DBHelper import MyHelper


class RARPDao:
    # 支出
    @classmethod
    def to_pay_dict(cls, data):
        result = []
        for row in data:
            res = {'supplierId': row[0], 'purchaseId': row[1], 'pay': row[2], 'date': row[3]}
            result.append(res)
        return result

    # 收到
    @classmethod
    def to_receive_dict(cls, data):
        result = []
        for row in data:
            res = {'customerId': row[0], 'sellId': row[1], 'receive': row[2], 'date': row[3]}
            result.append(res)
        return result

    # 应支出
    @classmethod
    def to_purchase_pay_dict(cls, data):
        result = []
        for row in data:
            res = {'supplierId': row[0], 'purchaseId': row[1], 'total': row[2], 'remain': row[3], 'reason': row[4],
                   'date': row[5]}
            result.append(res)
        return result

    # 应收入
    @classmethod
    def to_sell_receive_dict(cls, data):
        result = []
        for row in data:
            res = {'customerId': row[0], 'sellId': row[1], 'total': row[2], 'remain': row[3], 'reason': row[4],
                   'date': row[5]}
            result.append(res)
        return result
