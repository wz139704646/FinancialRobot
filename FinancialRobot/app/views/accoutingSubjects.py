from flask import Blueprint, request, jsonify
from app.utils.DBHelper import MyHelper
from app.utils.json_util import *
import json
from app.dao.AccountingSubjectDao import AccountingSubjectDao
from app.dao.GeneralVoucherDao import GeneralVoucherDao


accounting_subjects = Blueprint('accounting_subjects', __name__)
a_s_dao = AccountingSubjectDao()
g_v_dao = GeneralVoucherDao()


def get_top_subject_code(subject_code):
    return subject_code[:4]


# def


# 获取科目种类
@accounting_subjects.route("/finance/subject/getTypes", methods=["GET", "POST"])
def subject_get_types():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    if cond and cond.get('subject_code'):
        res = a_s_dao.query_subject_type_rate(cond.get('subject_code'))
    else:
        res = a_s_dao.query_all_types()

    if res:
        return jsonify(return_success(res))
    else:
        return jsonify(return_unsuccess('无法获取相关科目类别信息'))


# 获取科目
@accounting_subjects.route("/finance/subject/getSubjects", methods=["GET", "POST"])
def subject_get_with_options():
    _method = request.method
    if _method == 'GET':
        options = request.args
    else:
        options = request.json

    subjects = a_s_dao.query_subject(options)
    if subjects:
        return jsonify(return_success(a_s_dao.accounting_subject_to_dict(subjects)))
    else:
        return jsonify(return_unsuccess('无相关科目'))


def set_sub_recursive(header_nodes):
    for i in range(len(header_nodes)):
        subs = a_s_dao.query_subject({'superior_subject_code': header_nodes[i].get('subject_code')})
        header_nodes[i]['subs'] = a_s_dao.accounting_subject_to_dict(subs or [])
        if len(header_nodes[i]['subs']):
            set_sub_recursive(header_nodes[i]['subs'])


# 获取科目的树形展示数据
@accounting_subjects.route("/finance/subject/getSubjectsTree", methods=["GET", "POST"])
def subject_get_tree():
    subjects = a_s_dao.query_subject({'superior_subject_code': None})
    if subjects:
        tree = a_s_dao.accounting_subject_to_dict(subjects)
        set_sub_recursive(tree)
        return jsonify(return_success(tree))
    else:
        return jsonify(return_unsuccess('获取到的科目信息为空'))


@accounting_subjects.route("/finance/subject/getSubSubjects", methods=["POST", "GET"])
def subject_get_subs():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json
    if cond and cond.get('subject_code'):
        subs = a_s_dao.accounting_subject_to_dict(a_s_dao.query_sub_subject(cond.get('subject_code')))
        if len(subs):
            subs.sort(key=lambda item: item.get('subject_code'))
            return jsonify(return_success(subs))
        else:
            return jsonify(return_unsuccess('该科目无子科目'))
    else:
        return jsonify(return_unsuccess('未提供科目代码'))


@accounting_subjects.route("/finance/subject/getTop", methods=["GET", "POST"])
def subject_get_top_subject():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    if not cond.get('subject_code'):
        return jsonify(return_unsuccess('参数不全，未给出科目代码'))
    top = a_s_dao.query_top_subject(cond.get('subject_code'))
    if top:
        return jsonify(return_success(top))
    else:
        return jsonify(return_unsuccess('无相关科目信息'))


@accounting_subjects.route("/finance/subject/getNewCode", methods=["GET", "POST"])
def subject_get_new_code():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json
    if cond and cond.get('subject_code'):
        code = cond.get('subject_code')
        rows = a_s_dao.query_subject({'superior_subject_code': code})
        if rows:
            lv1_subs = a_s_dao.accounting_subject_to_dict(rows)
            suffix = []
            nums = []
            for sub in lv1_subs:
                suffix.append((sub['subject_code'])[4:])
                nums.append(int(sub['subject_code']))
            new_code = code
            # 寻找01-99中是否有没有使用的，有则对code直接进行凭借作为新代码
            for i in range(1, 100):
                if str(i).zfill(2) not in suffix:
                    new_code += str(i).zfill(2)
                    break
            # 01-99均已使用，寻找数字上最大的科目，数字+1转字符串
            if new_code == code:
                new_code = str(max(nums)+1)
        else:
            # 无子科目，则直接在科目代码后添加01
            new_code = code + '01'

        if new_code == code or not new_code.startswith(code):
            return jsonify(return_unsuccess('明细科目已达预期上限，需自行添加明细科目代码'))
        else:
            return jsonify(return_success(new_code))
    else:
        return jsonify(return_unsuccess('参数信息不完整'))


@accounting_subjects.route("/finance/subject/addSubject", methods=["POST"])
def subject_add_subject():
    _json = request.json

    # 检查该科目的上级科目是否已用于凭证录制
    if _json.get('superior_subject_code') is not None:
        entries = g_v_dao.query_voucher_entries({'subject_code': _json.get('superior_subject_code')})
        if entries:
            return jsonify(return_unsuccess('科目'+_json.get('superior_subject_code')+'已用于凭证录制，不能添加明细科目'))

    # 直接使用json作为插入数据
    res = a_s_dao.insert_subject(_json)
    if res[0]:
        return jsonify(return_success(res[1]))
    else:
        return jsonify(return_unsuccess(res[1]))


@accounting_subjects.route("/finance/subject/getBalance", methods=["GET", "POST"])
def subject_get_balance():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    balance = a_s_dao.query_subject_balance(cond)
    if len(balance):
        return json.dumps(return_success(balance), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess("无相关科目余额信息"))


@accounting_subjects.route("/finance/subject/getBalanceWithTimeRange", methods=["GET", "POST"])
def subject_get_balance_with_time_range():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    balance = a_s_dao.query_subject_balance_by_time_range(cond, cond.get('low'), cond.get('up'))
    if len(balance):
        return json.dumps(return_success(balance), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess('该条件下无相关科目信息'))


@accounting_subjects.route("/finance/subject/setBalance", methods=["POST"])
def subject_set_balance():
    data = request.json
    update_res = a_s_dao.update_subject_balance(data)
    if update_res[0]:
        return json.dumps(return_success({'old': update_res[1], 'new': update_res[2]}), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess(update_res[1]))


@accounting_subjects.route("/finance/subject/addBalance", methods=["POST"])
def subject_add_balance():
    data = request.json
    insert_res = a_s_dao.insert_subject_balance(data)
    if insert_res[0]:
        return json.dumps(return_success(insert_res[1]), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess(insert_res[1]))

