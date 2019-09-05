import datetime
import time
import uuid

from app.utils.DBHelper import MyHelper


class ARAPDao:

    # 应支出
    @classmethod
    def to_purchase_pay_dict(cls, data):
        result = []
        for row in data:
            res = {'supplierId': row[0], 'purchaseId': row[1], 'total': row[2], 'reason': row[3],
                   'date': row[4], 'companyId': row[5], 'remain': row[6]}
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

    def query_purchase_pay(self, purchaseId, days):
        _param = []
        _sql = "select * from PurchasePayment where 1 = 1 "
        if purchaseId:
            _sql += " and purchaseId = %s"
            _param.append(purchaseId)
        if days:
            delta = datetime.timedelta(days=days)
            now = datetime.datetime.now()
            _date = now - delta
            _sql += " and date >= %s and date <=%s"
            _param.append(_date)
            _param.append(now)
        _sql += ' order by date DESC'
        connection = MyHelper()
        rows = connection.executeQuery(_sql, _param)
        res = []
        for row in rows:
            remain = self.query_purchase_pay_remain(row[1])
            lis = list(row)
            lis.append(remain)
            res.append(lis)
        return res

    def query_purchase_pay_remain(self, purchaseId):
        connection = MyHelper()
        rows = connection.executeQuery("select pay from Payment where purchaseId = %s", [purchaseId])
        total = 0
        if len(rows) == 0:
            pass
        else:
            for row in rows:
                total = total + row[0]
        rows = connection.executeQuery("select total from PurchasePayment where purchaseId = %s",
                                       [purchaseId])
        return rows[0][0] - total

    # 应收入
    @classmethod
    def to_sell_receive_dict(cls, data):
        result = []
        for row in data:
            res = {'customerId': row[0], 'sellId': row[1], 'total': row[2], 'reason': row[3],
                   'date': row[4], 'companyId': row[5], 'remain': row[6]}
            result.append(res)
        return result

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

    def query_sell_receive(self, sellId, days):
        _param = []
        _sql = "select * from SellReceive where 1 = 1 "
        if sellId:
            _sql += " and sellId = %s"
            _param.append(sellId)
        if days:
            delta = datetime.timedelta(days=days)
            now = datetime.datetime.now()
            _date = now - delta
            _sql += " and date >= %s and date <=%s"
            _param.append(_date)
            _param.append(now)
        _sql += ' order by date DESC'
        connection = MyHelper()
        rows = connection.executeQuery(_sql, _param)
        res = []
        for row in rows:
            remain = self.query_sell_receive_remain(row[1])
            lis = list(row)
            lis.append(remain)
            res.append(lis)
        return res

    def query_sell_receive_remain(self, sellId):
        connection = MyHelper()
        # 目前收到的金额
        rows = connection.executeQuery("select receive from Receive where sellId = %s", [sellId])
        total = 0
        if len(rows) == 0:
            pass
        else:
            for row in rows:
                total = total + row[0]
        # 期望收到的金额
        rows = connection.executeQuery("select total from SellReceive where sellId = %s",
                                       [sellId])
        return rows[0][0] - total

    # 支出
    @classmethod
    def to_pay_dict(cls, data):
        result = []
        for row in data:
            res = {'id': row[0], 'purchaseId': row[1], 'pay': row[2], 'date': row[3], 'status': row[5],
                   'bank_name': row[6], 'clear_form': row[7]}
            result.append(res)
        return result

    def add_payment(self, purchaseId, amount, date, bank_name, clear_form):
        connection = MyHelper()
        _id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
        rows = connection.executeQuery("select companyId from Purchase where id = %s", [purchaseId])
        row = connection.executeUpdate("insert into Payment (id, purchaseId, pay, date, companyId,bankName,clearForm)"
                                       " values (%s,%s,%s,%s,%s,%s,%s)",
                                       [_id, purchaseId, amount, date, rows[0][0], bank_name, clear_form])

        res = {"row": row, "id": _id.__str__()}
        return res

    def query_payment(self, _id, purchaseId=None, days=None):
        _param = []
        _sql = "select * from Payment where 1 = 1"
        if _id:
            _sql += " and id = %s"
            _param.append(_id)
            connection = MyHelper()
            return connection.executeQuery(_sql, _param)
        if purchaseId:
            _sql += " and purchaseId = %s"
            _param.append(purchaseId)
        if days:
            delta = datetime.timedelta(days=days)
            now = datetime.datetime.now()
            _date = now - delta
            _sql += " and date >= %s and date <=%s"
            _param.append(_date)
            _param.append(now)
        _sql += ' order by date DESC'
        connection = MyHelper()
        return connection.executeQuery(_sql, _param)

    def check_payment(self, _id):
        connection = MyHelper()
        connection.executeUpdate("update Payment set status = 1 where id=%s", [_id])
        return self.query_payment(_id)

    # 收到 Receive
    @classmethod
    def to_receive_dict(cls, data):
        result = []
        for row in data:
            res = {'id': row[0], 'sellId': row[1], 'receive': row[2], 'date': row[3], 'status': row[5],
                   'bank_name': row[6], 'clear_form': row[7]}
            result.append(res)
        return result

    def add_receive(self, sellId, amount, date, bank_name, clear_form):
        connection = MyHelper()
        _id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
        rows = connection.executeQuery("select companyId from Sell where id = %s", [sellId])
        row = connection.executeUpdate("insert into Receive (id, sellId, receive, date, companyId,bankName,clearForm)"
                                       " values (%s,%s,%s,%s,%s,%s,%s)",
                                       [_id, sellId, amount, date, rows[0][0], bank_name, clear_form])
        res = {"row": row, "id": _id.__str__()}
        return res

    def query_receive(self, _id, sellId=None, days=None):
        _param = []
        _sql = "select * from Receive where 1 = 1"
        if _id:
            _sql += " and id = %s"
            _param.append(_id)
            connection = MyHelper()
            return connection.executeQuery(_sql, _param)
        if sellId:
            _sql += " and purchaseId = %s"
            _param.append(sellId)
        if days:
            delta = datetime.timedelta(days=days)
            now = datetime.datetime.now()
            _date = now - delta
            _sql += " and date >= %s and date <=%s"
            _param.append(_date)
            _param.append(now)
        _sql += ' order by date DESC'
        connection = MyHelper()
        return connection.executeQuery(_sql, _param)

    def check_receive(self, _id):
        connection = MyHelper()
        connection.executeUpdate("update Receive set status = 1 where id=%s", [_id])
        return self.query_receive(_id)
