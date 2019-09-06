import unittest
import asyncio
import jwt, datetime, time
import app.config as config
import os
import yaml
from app.utils.DBHelper import MyHelper
from app.dao.AccountingSubjectDao import AccountingSubjectDao
from app.utils.features import get_permission
from app.dao.GeneralVoucherDao import GeneralVoucherDao
import xlwings as xw
import numpy as np
import imgkit
from app.utils.finance_utils import *
from app.views.general_voucher import magnitude_digit
from app.utils.pic_str import *


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

class ZjjTesst(unittest.TestCase):

    def test1(self):
        asyncio.run(main())


    def test2(self):
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        payload = {
            'exp': expire_time,
            'iat': datetime.datetime.utcnow(),
            'data': {'hhh': 123},
        }
        encoded = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
        token = str(encoded, encoding='ascii')
        print('token encoded: '+token)
        time.sleep(5.5)
        try:
            payload1 = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
            print('time is: '+str(int(time.time())))
            print('token decoded:')
            print(payload1)
        except jwt.ExpiredSignatureError:

            print('token expired!')

    def test3(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        relative_dir = '../app/static/sql/finance_tbls.sql'
        targetdir = os.path.join(basedir, relative_dir)
        with open(targetdir) as fr:
            for a in fr.read().split(';'):
                print(a)
                print('----------------------------------------------')
        pass

    def test4(self):
        conn = MyHelper()
        basedir = os.path.abspath(os.path.dirname(__file__))
        relative_url = '../app/static/sql/finance_tbls.sql'
        target_url = os.path.join(basedir, relative_url)
        conn.executeCreate(filename=target_url)

    def test5(self):
        # AccountingSubjectDao Test
        self.test4()
        conn = MyHelper()
        # conn.executeUpdate('insert into accounting_subjects(subject_code, name, type)'
        #                    'values("1002", "银行存款", "资产类")')
        rows = conn.executeQuery(
            sql="select type, type_detail from accounting_subjects "
                "where subject_code = %s",
            param=['1002']
        )
        print(list(rows))

    def test6(self):
        test = ['100106']
        dict = {}
        dict['type'] = None
        print(dict)
        dao = AccountingSubjectDao()
        print(dao.query_subject({'subject_code':'1002'}))
        print(dao.insert_subject({
            'subject_code': '1002002',
            'name': '银行存款-花旗银行',
            'superior_subject_code': '1002'
        }))

    def test7(self):
       print(MyHelper().executeUpdateTransaction(
           sqls=["insert into accounting_subjects(subject_code, name, superior_subject_code, type, type_detail)"
                 " values(%s, %s, %s, %s, %s)",
                 "insert into accounting_subjects(subject_code, name, superior_subject_code, type, type_detail)"
                 " values(%s, %s, %s, %s, %s)"],
           params=[
               ["1009", "???", None, "资产类", None],
               ["100901", "??????", "1009", "资产类", None]
           ]
       ))

    def test8(self):
        dao = GeneralVoucherDao()
        voucher = dao.general_voucher_to_dict(dao.query_voucher({'voucher_no': '201908001'}))
        print(type(voucher[0].get('record_date')))
        now = datetime.date(2019, 8, 1)
        print(now.strftime('%Y%m%d'))

    def test9(self):
        a = {'123': 'sdasds', '4503': 'asdasdasds'}
        print(list(a.values()))
        print(a.get(None))
        print(list({}.values()))
        dao = AccountingSubjectDao()
        print(dao.query_all_types())

    # 只能在windows下使用，放弃
    def test_xlwings_1(self):
        f = xw.Book('')
        sheet = f.sheets.add()
        sheet.range('A1').value = np.zeros([2000, 1200]) + 65536
        f.close()

    def test_html2img(self):
        path_wk = r'D:\Application\wkhtmltox\bin\wkhtmltoimage.exe'  # 安装位置
        imgkit_config = imgkit.config(wkhtmltoimage=path_wk)

        imgkit.from_url('http://baidu.com', 'D://out.jpg', config=imgkit_config)

    def test_money_cap(self):
        money = 1300.8
        print(capitalized_amount_of_money(money))
        print(magnitude_digit(122.2, -1))
        print(Pic_str().create_uuid())
        print(type(remove_exponent(1.0)))
