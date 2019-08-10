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


@accounting_subjects.route("/finance/subject/getAll", methods=["GET", "POST"])
def subject_get_all():
    rows = dao.query_subject()
    if rows:
        all_subjects = dao.accounting_subject_to_dict(rows)
        return jsonify(return_success(all_subjects)), 200
    else:
        return jsonify(return_unsuccess('无法获取科目信息'))


@accounting_subjects.route("/finance/subject/get4CertainType", methods=["GET", "POST"])
def subject_get_for_certain_type():
    method = request.method
    sub_type = ''
    if method == 'GET':
        sub_type = request.args.get('type')
    elif method == 'POST':
        sub_type = request.json.get('type')

    if not sub_type:
        return jsonify(return_unsuccess('查询参数不全'))
    else:
        subs = dao.query_subject({'type': sub_type})
        if subs:
            return jsonify(return_success(dao.accounting_subject_to_dict(subs)))
        else:
            return jsonify(return_unsuccess('无法获取科目信息'))


@accounting_subjects.route("/finance/subject/getAllGrouped", methods=["GET", "POST"])
def subject_get_grouped():
    types = dao.query_all_types()
    if types:
        res = []
        for type in types:
            subs = dao.query_subject({'type': type})
            if subs:
                res.append({'type': type, 'subjects': dao.accounting_subject_to_dict(subs)})
            else:
                res.append({'type': type, 'subjects': []})
        return jsonify(return_success(res)), 200
    else:
        return jsonify(return_unsuccess('无法获取科目类别信息'))
