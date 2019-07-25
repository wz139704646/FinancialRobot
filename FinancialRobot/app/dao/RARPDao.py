import time
import uuid

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

    def add_purchase_pay(self, purchaseId, reason):
        connection = MyHelper()
        rows = connection.executeQuery(
            "select Purchase.supplierId,Purchase.companyId,Purchase.purchasePrice,Purchase.number,Purchase.date "
            "from Purchase where Purchase.id = %s",
            [purchaseId])
        total = 0
        for row in rows:
            total = total + row[2] * row[3]
        return connection.executeUpdate(
            "insert into PurchasePayment (supplierId, purchaseId, total, reason, date, companyId)"
            "values (%s,%s,%s,%s,%s,%s)",
            [rows[0][0], purchaseId, total, reason, rows[0][4], rows[0][1]])

    def add_sell_receive(self, sellId, reason):
        connection = MyHelper()
        rows = connection.executeQuery("select customerId,sumprice,companyId,Sell.date"
                                       " from Sell where id = %s", [sellId])
        total = 0
        for row in rows:
            total = total + row[1]
        return connection.executeUpdate(
            "insert into SellReceive (customerId, sellId, total, reason, date, companyId)"
            "values (%s,%s,%s,%s,%s,%s)",
            [rows[0][0], sellId, total, reason, rows[0][3], rows[0][2]])

    def add_payment(self, purchaseId, amount, date):
        connection = MyHelper()
        id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
        rows = connection.executeQuery("select companyId from Purchase where id = %s", [purchaseId])
        return connection.executeUpdate("insert into Payment (id, purchaseId, pay, date, companyId)"
                                        " values (%s,%s,%s,%s,%s)",
                                        [id,purchaseId, amount, date, rows[0][0]])

    def add_receive(self, sellId, amount, date):
        connection = MyHelper()
        id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
        rows = connection.executeQuery("select companyId from Sell where id = %s", [sellId])
        return connection.executeUpdate("insert into Receive (id, sellId, receive, date, companyId)"
                                        " values (%s,%s,%s,%s,%s)",
                                        [id,sellId, amount, date, rows[0][0]])

    def query_purchase_pay_remain(self, purchaseId):
        connection = MyHelper()
        rows = connection.executeQuery("select pay from Payment where purchaseId = %s", [purchaseId])
        total = 0
        for row in rows:
            total = total + row[0]
        rows = connection.executeQuery("select total from PurchasePayment where purchaseId = %s",
                                       [purchaseId])
        return rows[0][0] - total

    def query_sell_receive_remain(self, sellId):
        connection = MyHelper()
        # 目前收到的金额
        rows = connection.executeQuery("select receive from Receive where sellId = %s", [sellId])
        total = 0
        for row in rows:
            total = total + row[0]
        # 期望收到的金额
        rows = connection.executeQuery("select total from SellReceive where sellId = %s",
                                       [sellId])
        return rows[0][0] - total
