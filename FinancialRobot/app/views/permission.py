from flask import Blueprint, request
from app.dao.UserDao import UserDao
from app.utils.auth import check_token
from app.utils.json_util import *

permission = Blueprint("permission", __name__)
permission.secret_key = 'secret_key_permission'


@permission.before_request
@check_token
def res():
    pass


@permission.route('/addPermissionByFeatures', methods=['POST'])
def addPermissionByFeatures():
    account = request.json.get('account')
    features = request.json.get('features')
    try:
        UserDao().add_permission_by_features(account, features)
        return json.dumps(return_success('ok'))
    except Exception as e:
        return json.dumps(return_unsuccess('Add Permission Failed: ' + str(e)))


@permission.route('/delPermissionByFeatures', methods=['POST'])
def delPermissionByFeatures():
    account = request.json.get('account')
    features = request.json.get('features')
    try:
        UserDao().del_permission_by_features(account, features)
        return json.dumps(return_success('ok'))
    except Exception as e:
        return json.dumps(return_unsuccess('Del Permission Failed: ' + str(e)))


@permission.route('/addPermissionByRole', methods=['POST'])
def addPermissionByRole():
    account = request.json.get('account')
    role = request.json.get('role')
    try:
        UserDao().add_permission_by_role(account, role)
        return json.dumps(return_success('ok'))
    except Exception as e:
        return json.dumps(return_unsuccess('Add Permission Failed: ' + str(e)))


@permission.route('/queryPermission', methods=['POST'])
def queryPermission():
    account = request.json.get('account')
    try:
        res = UserDao().query_permission(account)
        return json.dumps(return_success(UserDao.to_permission_dict(res)))
    except Exception as e:
        return json.dumps(return_unsuccess('Query Permission Failed: ' + str(e)))
