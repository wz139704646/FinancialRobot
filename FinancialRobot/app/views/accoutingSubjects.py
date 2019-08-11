from flask import Blueprint, request, jsonify
from app.utils.DBHelper import MyHelper
from app.dao.AccountingSubjectDao import AccountingSubjectDao
from app.utils.json_util import *
import json
from app.dao.AccountingSubjectDao import AccountingSubjectDao


accounting_subjects = Blueprint('accounting_subjects', __name__)
dao = AccountingSubjectDao()


def get_top_subject_code(subject_code):
    return subject_code[:4]


# 获取科目种类
@accounting_subjects.route("/finance/subject/getTypes", methods=["GET", "POST"])
def subject_get_grouped():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    if cond and cond.get('subject_code'):
        res = dao.query_subject_type_rate(cond.get('subject_code'))
    else:
        res = dao.query_all_types()

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

    subjects = dao.query_subject(options)
    if subjects:
        return jsonify(return_success(dao.accounting_subject_to_dict(subjects)))
    else:
        return jsonify(return_unsuccess('无相关科目'))


@accounting_subjects.route("/finance/subject/getNewCode", methods=["GET", "POST"])
def subject_get_new_code():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json
    if cond and cond.get('subject_code'):
        code = cond.get('subject_code')
        rows = dao.query_lv_one_sub_subject(code)
        if rows:
            lv1_subs = dao.accounting_subject_to_dict(rows)
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
    # TODO 检查该科目是否已用于凭证录制

    # 直接使用json作为插入数据
    res = dao.insert_subject(_json)
    if res[0]:
        return jsonify(return_success(res[1]))
    else:
        return jsonify(return_unsuccess(res[1]))
