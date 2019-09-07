from flask import Blueprint, request, jsonify, render_template
from app.utils.DBHelper import MyHelper
from app.utils.json_util import *
from app.utils.finance_utils import *
from app.utils.jinja2_utils import render_without_request
import json
from app.dao.AccountingSubjectDao import AccountingSubjectDao
from app.dao.GeneralVoucherDao import GeneralVoucherDao
from functools import reduce
from app.utils.finance_utils import *
from app.utils.pic_str import *
import math
import imgkit
import os
from werkzeug.utils import secure_filename
import threading


general_voucher = Blueprint('general_voucher', __name__)
# general_voucher.add_app_template_filter(magnitude_digit, 'magnitude_digit')
g_v_dao = GeneralVoucherDao()
a_s_dao = AccountingSubjectDao()
max_entries_in_one_voucher_pic = 6

UPLOAD_FOLDER = '../static/img/voucher'
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB


def get_vouchers(cond, date_ranged=False, spec_time=False):
    if date_ranged:
        vouchers = g_v_dao.query_voucher_by_date_range(cond, cond.get('low'), cond.get('up'))
    elif spec_time:
        time = cond.get('time')
        if not time or not len(str(time)) == 6:
            return
        time = str(time)
        year = time[:4]
        month = time[4:]
        day_low = '01'
        day_up = '31'
        vouchers = g_v_dao.query_voucher_by_date_range(cond, year+month+day_low, year+month+day_up)
    else:
        vouchers = g_v_dao.query_voucher(cond)
    if vouchers:
        vouchers = g_v_dao.general_voucher_to_dict(vouchers)
        # 为每一个凭证添加分录字段
        for v in vouchers:
            v['entries'] = g_v_dao.voucher_entry_to_dict(
                g_v_dao.query_voucher_entries({'voucher_no': v.get('voucher_no')}) or []
            )
            v['abstract'] = v['entries'][0].get('abstract') if len(v['entries']) else ""
            v['total'] = reduce(lambda acc, cur: acc + cur.get('total') if cur.get('credit_debit') == '借' else acc,
                                v['entries'], 0)
        return vouchers


@general_voucher.route("/finance/voucher/getVouchers", methods=["GET", "POST"])
def voucher_get_with_options():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json
    # 根据查询条件中有关日期限制条件的不同，按条件查询凭证信息
    if cond.get('date'):
        vouchers = get_vouchers(cond)
    elif all([cond.get('low'), cond.get('up')]):
        vouchers = get_vouchers(cond, date_ranged=True)
    elif cond.get('time'):
        vouchers = get_vouchers(cond, spec_time=True)
    else:
        vouchers = get_vouchers(cond)

    if vouchers:
        return json.dumps(return_success(vouchers), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess('无相关凭证信息，请检查查询条件'))


def update_subject_balance_on_voucher_update(time, entries_del=[], entries_add=[]):
    updates = []
    for entry in entries_del or []:
        updates.append({
            'subject_code': entry.get('subject_code'),
            "time": time,
            "credit" if entry.get('credit_debit') == '借' else "debit": {
                'way': 'update',
                'value': -entry.get('total')
            }
        })
    for entry in entries_add or []:
        updates.append({
            'subject_code': entry.get('subject_code'),
            "time": time,
            "credit" if entry.get('credit_debit') == '借' else "debit": {
                'way': 'update',
                'value': entry.get('total')
            }
        })
    update_res = a_s_dao.update_subject_balance(updates)
    if not update_res[0]:
        # 更新失败，返回错误信息
        return False, update_res[1]
    # 更新成功
    return True, update_res[1]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@general_voucher.route("/finance/voucher/addAttachment", methods=["POST"])
def voucher_add_attachment():
    form_ = request.form
    voucher_no = form_.get('voucher_no')
    if not voucher_no:
        return jsonify(return_unsuccess('上传失败，缺少对应的凭证编号'))

    # 获取图片并保存至本地
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f, = request.files.values()
    size = len(f.read())
    print(size)
    f.seek(0)
    if f and allowed_file(f.filename):
        if size <= MAX_CONTENT_LENGTH:
            fname = secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]
            new_filename = voucher_no + '_' + Pic_str().create_uuid() + '.' + ext
            # 更新photo
            try:
                # 保存图片到本地
                f.save(os.path.join(file_dir, new_filename))
                f.close()
                g_v_dao.insert_voucher_attachment({'voucher_no': voucher_no, 'attachment_url': new_filename})
                return json.dumps(return_success(new_filename), ensure_ascii=False)
            except Exception as e:
                return jsonify(return_unsuccess('附件上传失败'))
        else:
            return json.dumps(return_unsuccess("文件大小超出5MB"), ensure_ascii=False)
    else:
        return json.dumps(return_unsuccess("文件格式不正确"), ensure_ascii=False)


@general_voucher.route("/finance/voucher/setAttachment", methods=["POST"])
def voucher_set_attachment():
    _json = request.json

    if not all([_json.get('voucher_no'), _json.get('attachment_url'), _json.get('data')]):
        return jsonify(return_unsuccess('缺少必要参数'))

    update_res = g_v_dao.update_voucher_attachment(_json.get('voucher_no'),
                                                   _json.get('attachment_url'), _json.get('data'))
    if not update_res[0]:
        return jsonify(return_unsuccess('更新附件信息失败'))
    res = {'old': update_res[1], 'new': update_res[2]}
    errMsg = ''

    file_dir = os.path.join(basedir, UPLOAD_FOLDER)
    try:
        os.remove(os.path.join(file_dir, '%s' % _json.get('attachment_url')))
    except Exception as e:
        errMsg = '删除附件图片{}失败'.format(_json.get('attachment_url'))

    if errMsg:
        res['errMsg'] = errMsg

    return json.dumps(return_success(errMsg), ensure_ascii=False)


@general_voucher.route("/finance/voucher/delAttachment", methods=["POST"])
def voucher_del_attachment():
    _json = request.json

    if not _json.get('voucher_no'):
        return jsonify(return_unsuccess('缺少必要参数：附件对应凭证编号'))

    file_dir = os.path.join(basedir, UPLOAD_FOLDER)

    attachments = g_v_dao.query_voucher_attachments(_json)
    if attachments:
        attachments = g_v_dao.voucher_attachment_to_dict(attachments)
    else:
        return jsonify(return_unsuccess('无相关附件信息'))

    del_res = g_v_dao.delete_voucher_attachment(_json)
    if del_res[0]:
        del_res = del_res[1]
    else:
        return jsonify(return_unsuccess('删除附件信息失败'))
    res = {'old': del_res}

    errMsgs = []

    for att in attachments:
        try:
            os.remove(os.path.join(file_dir, '%s' % att.get('attachment_url')))
        except Exception as e:
            errMsgs.append('删除附件图片{}失败'.format(att.get('attachment_url')))

    res['errMsgs'] = errMsgs
    return json.dumps(return_success(res), ensure_ascii=False, cls=DecimalEncoder)


@general_voucher.route("/finance/voucher/getVoucherWithAttachment", methods=["GET", "POST"])
def voucher_get_with_attachment():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    if cond.get('for_voucher') is not None:
        cond.pop('for_voucher')

    if cond.get('date'):
        vouchers = get_vouchers(cond)
    elif all([cond.get('low'), cond.get('up')]):
        vouchers = get_vouchers(cond, date_ranged=True)
    elif cond.get('time'):
        vouchers = get_vouchers(cond, spec_time=True)
    else:
        vouchers = get_vouchers(cond)

    if vouchers:
        # 添加凭证分录信息和摘要、总金额、附件
        for v in vouchers:
            v['entries'] = g_v_dao.voucher_entry_to_dict(
                g_v_dao.query_voucher_entries({'voucher_no': v.get('voucher_no')}) or []
            )
            v['abstract'] = v['entries'][0].get('abstract') if len(v['entries']) else ""
            v['total'] = reduce(lambda acc, cur: acc + cur.get('total') if cur.get('credit_debit') == '借' else acc,
                                v['entries'], 0)
            v['attachments'] = []
            att = g_v_dao.voucher_attachment_to_dict(g_v_dao.query_voucher_attachments({'voucher_no': v.get('voucher_no')}) or [])
            for a in att:
                v['attachments'].append({
                    'voucher_no': a.get('voucher_no'),
                    'attachment_url': a.get('attachment_url'),
                    'for_voucher': a.get('for_voucher')
                })
        return json.dumps(return_success(vouchers), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess('无相关凭证信息'))


@general_voucher.route("/finance/voucher/getAttachment", methods=["GET", "POST"])
def voucher_get_attachment():
    _method = request.method
    if _method == 'GET':
        cond = request.args
    else:
        cond = request.json

    att = g_v_dao.query_voucher_attachments(cond)
    if att:
        att = g_v_dao.voucher_attachment_to_dict(att)
        return json.dumps(return_success(att), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess('无相关附件信息'))


def cal_total_credit_debit(acc, cur):
    if cur.get('credit_debit') == '借':
        acc[0] = acc[0] + cur.get('total')
    else:
        acc[1] = acc[1] + cur.get('total')
    return acc


def voucher_gen_save(voucher_no):
    """
    生成并保存凭证图片
    :param voucher_no: 凭证编号
    :return: tuple类型，是否成功生成并保存，第二个元素为保存的图片名，或失败时的原因
    """
    # 检查目录是否存在
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    vouchers = get_vouchers({'voucher_no': voucher_no})
    if not vouchers:
        return False, '无相关凭证信息，请检查查询条件'

    # 根据分录数目决定凭证张数
    entries = vouchers[0].get('entries')
    num_voucher = math.ceil(len(entries) / max_entries_in_one_voucher_pic)
    renders = []

    for i in range(num_voucher):
        # 渲染凭证
        end = len(entries) if max_entries_in_one_voucher_pic * (i + 1) > len(
            entries) else max_entries_in_one_voucher_pic * (i + 1)
        entries_cur = entries[max_entries_in_one_voucher_pic * i:end]
        credit_total, debit_total = reduce(cal_total_credit_debit, entries_cur, [0, 0])
        cur_total = max(credit_total, debit_total)
        rendered = render_without_request(
            template_name='voucher_template.html', filters={'magnitude_digit': magnitude_digit},
            voucher_type='记账凭证', num_attachments=vouchers[0].get('attachments_number'),
            date=vouchers[0].get('date'), voucher_no=vouchers[0].get('voucher_no'), num_voucher_cur=i + 1,
            num_vouchers=num_voucher, entries=entries_cur,
            total_cap=capitalized_amount_of_money(cur_total), credit_total=credit_total,
            debit_total=debit_total
        )

        new_filename = voucher_no + '_' + Pic_str().create_uuid() \
                       + 'voucher({})'.format(i + 1) + '.' + 'png'
        store_path = os.path.join(file_dir, new_filename)
        # Windows下
        # path_wk = r'D:\Application\wkhtmltox\bin\wkhtmltoimage.exe'  # 安装位置
        # imgkit_config = imgkit.config(wkhtmltoimage=path_wk)
        # if imgkit.from_string(rendered, store_path, config=imgkit_config):
        #     renders.append(new_filename)
        if imgkit.from_string(rendered, store_path):
            renders.append(new_filename)
        else:
            for file in renders:
                try:
                    os.remove(file)
                except Exception as e:
                    print(e)
            return False, '凭证生成失败'

    # 删除已有的凭证的图片
    suc, attachment = g_v_dao.delete_voucher_attachment(voucher_no, {'for_voucher': 1})
    for att in attachment:
        try:
            os.remove(os.path.join(file_dir, '%s' % att.get('attachment_url')))
        except Exception as e:
            print(e)
    # 重新添加凭证图片
    for v in renders:
        g_v_dao.insert_voucher_attachment({
            'voucher_no': voucher_no,
            'for_voucher': 1,
            'attachment_url': v
        })

    return True, renders


@general_voucher.route("/finance/voucher/genVoucher", methods=["GET", "POST"])
def voucher_gen_with_no():
    _method = request.method
    if _method == 'GET':
        args = request.args
    else:
        args = request.json
    if not args.get('voucher_no'):
        return jsonify(return_unsuccess('请求参数不全'))

    gen_res = voucher_gen_save(args.get('voucher_no'))
    if gen_res[0]:
        return json.dumps(return_success(gen_res[1]))
    else:
        return jsonify(return_unsuccess(gen_res[1]))


@general_voucher.route("/finance/voucher/addVoucher", methods=["POST"])
def voucher_add():
    _json = request.json

    if not all([_json.get('date'), _json.get('entries')]):
        return jsonify(return_unsuccess('缺少参数日期或分录'))

    time = _json.get('date')
    time = ''.join(time.split('-')[:2]) if type(time) == str else time.strftime('%Y%m')
    entries = _json.get('entries')
    credit_tot = 0
    debit_tot = 0
    for entry in entries:
        if a_s_dao.query_subject({'superior_subject_code': entry.get('subject_code')}):
            return jsonify(return_unsuccess('不能在上级科目({})下录制凭证'.format(entry.get('subject_code'))))

        if not len(a_s_dao.query_subject_balance({'time': time, 'subject_code': entry.get('subject_code')})):
            a_s_dao.insert_subject_balance({'time': time, 'subject_code': entry.get('subject_code')})

        if entry.get('credit_debit') == '借':
            credit_tot = credit_tot + entry.get('total')
        else:
            debit_tot = debit_tot + entry.get('total')
    if credit_tot != debit_tot:
        return jsonify(return_unsuccess('添加失败，凭证借贷不平衡'))

    add_res = g_v_dao.insert_voucher(_json)
    if add_res[0]:
        # 凭证添加成功
        # 更新余额
        update_res = update_subject_balance_on_voucher_update(time, [], entries)
        if not update_res[0]:
            # 余额更新失败，将已添加的凭证删除
            g_v_dao.delete_voucher(add_res[1].get('voucher_no'))
            return jsonify(return_unsuccess(update_res[1]))
        # 凭证添加完成
        # 产生子线程生成凭证图片并保存
        t = threading.Thread(target=voucher_gen_save, name='gen_voucher', args=(add_res[1].get('voucher_no'),))
        t.start()

        return json.dumps(return_success(add_res[1]), cls=DecimalEncoder)
    else:
        return jsonify(return_unsuccess(add_res[1]))


@general_voucher.route("/finance/voucher/delVoucher", methods=["POST"])
def voucher_del_with_no():
    _json = request.json

    if _json.get('voucher_no'):
        # 删除凭证
        attachment = g_v_dao.query_voucher_attachments({'voucher_no': _json.get('voucher_no')})
        del_res = g_v_dao.delete_voucher(_json.get('voucher_no'))
        if del_res[0]:
            # 删除凭证时通过分录提交对应科目余额的变动
            old_data = del_res[1]
            update_res = update_subject_balance_on_voucher_update(
                time=old_data.get('date').strftime('%Y%m'), entries_del=old_data['entries']
            )
            # 删除失败，取消凭证删除，重新添加回去
            if not update_res[0]:
                g_v_dao.insert_voucher(old_data)
                return jsonify(return_unsuccess(update_res[1]))
            else:
                # 删除成功，返回原数据
                # 清除所有凭证附件
                file_dir = os.path.join(basedir, UPLOAD_FOLDER)
                if attachment:
                    attachment = g_v_dao.voucher_attachment_to_dict(attachment)
                for att in attachment:
                    try:
                        os.remove(os.path.join(file_dir, '%s' % att.get('attachment_url')))
                    except Exception as e:
                        print(e)
                return json.dumps(return_success(old_data), cls=DecimalEncoder)
        else:
            return jsonify(return_unsuccess(del_res[1]))
    else:
        return jsonify(return_unsuccess('参数不全，缺少凭证编号'))


@general_voucher.route("/finance/voucher/setVoucher", methods=["POST"])
def voucher_set_with_no():
    _json = request.json

    if not all([_json.get('voucher_no'), _json.get('changes')]):
        return jsonify(return_unsuccess('参数不全，缺少凭证编号或更改信息'))
    else:
        if not _json.get('changes').get('record_date'):
            _json['changes']['record_date'] = datetime.datetime.now()
        if _json.get('changes').get('entries'):
            credit_tot = 0
            debit_tot = 0
            for entry in _json.get('changes').get('entries'):
                if entry.get('credit_debit') == '借':
                    credit_tot = credit_tot + entry.get('total')
                else:
                    debit_tot = debit_tot + entry.get('total')
            if credit_tot != debit_tot:
                return jsonify(return_unsuccess('更新失败，凭证借贷不平衡'))
        set_res = g_v_dao.update_voucher(_json.get('voucher_no'), _json.get('changes'))
        if set_res[0]:
            old_data = set_res[1]
            new_data = set_res[2]
            if _json.get('changes').get('entries'):
                # 如果更新了分录，则将原分录信息和新分录信息的科目余额变动提交
                update_res = update_subject_balance_on_voucher_update(
                    old_data.get('date').strftime('%Y%m'),
                    entries_del=old_data.get('entries'),
                    entries_add=new_data.get('entries')
                )
                if not update_res[0]:
                    # 余额更新失败，将变动取消
                    g_v_dao.update_voucher(new_data.get('voucher_no'), old_data)
                    return jsonify(return_unsuccess(update_res[1]))
                # 分录更新成功，将对应的凭证图片重新生成
                t = threading.Thread(target=voucher_gen_save, name='voucher_gen', args=(new_data.get('voucher_no'),))
                t.start()
            return json.dumps(return_success({'old': old_data, 'new': new_data}), cls=DecimalEncoder)
        else:
            return jsonify(return_unsuccess(set_res[1]))
