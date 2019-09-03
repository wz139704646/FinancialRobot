from app.utils.features import get_permission
from app.utils.DBHelper import MyHelper


class UserDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {'account': row[0], 'companyId': row[2], 'ID': row[3], 'position': row[4]}
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        result = connection.executeQuery('select * from User')
        return result

    def add(self, account, password, companyid):
        connection = MyHelper()
        row = connection.executeUpdate('insert into User(account, \
        password, CompanyId) \
         values (%s,%s,%s)', [account, password, companyid])
        return row

    def query_by_account(self, account):
        helper = MyHelper()
        return helper.executeQuery("select * from User where account=%s", [account])

    def query_check_login(self, account, password):
        helper = MyHelper()
        return helper.executeQuery("select * from User where account=%s and password=%s ",
                                   [account, password])

    def query_by_openid_account(self, account, openid):
        _param = []
        _sql = "select * from User where 1=1"
        if account:
            _sql += " and account = %s"
            _param.append(account)
        if openid:
            _sql += " and openid = %s"
            _param.append(openid)
        helper = MyHelper()
        return helper.executeQuery(_sql, _param)

    def bind_wx(self, account, openid):
        helper = MyHelper()
        return helper.executeUpdate("update User set openid = %s where account = %s",
                                    [openid, account])

    def set_position(self, account, position):
        connection = MyHelper()
        return connection.executeUpdate('update User set position = %s where account = %s', [position, account])

    # 权限管理
    @classmethod
    def to_permission_dict(cls, data):
        res = []
        result = {'feature': res}
        for row in data:
            result['feature'].append(row[0])
        return result

    def query_permission(self, account):
        connection = MyHelper()
        return connection.executeQuery("select feature from Permission where account = %s", [account])

    def add_permission_by_features(self, account, features):
        connection = MyHelper()
        # 已有的权限
        _features = self.query_permission(account)
        # print(_features)
        for feature in features:
            # print(features)
            if (feature,) not in _features:
                connection.executeUpdate("insert into Permission (feature, account) VALUES (%s,%s)",
                                         [feature, account])
        return

    def del_permission_by_features(self, account, features):
        connection = MyHelper()
        # 已有的权限
        _features = self.query_permission(account)
        for feature in features:
            if (feature,) in _features:
                connection.executeUpdate("delete from Permission where feature=%s and account = %s",
                                         [feature, account])
        return

    def add_permission_by_role(self, account, role):
        roles = get_permission()['roles']
        # print(roles)
        for r in roles:
            if role == r['name']:
                self.add_permission_by_features(account, r['allow_feature'])
                return
        pass

    def del_permission_by_role(self, account, role):
        roles = get_permission()['roles']
        # print(roles)
        for r in roles:
            if role == r['name']:
                self.del_permission_by_features(account, r['allow_feature'])
                return
        pass
