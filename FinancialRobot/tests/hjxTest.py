#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import unittest

from app.dao.WareHouseDao import WareHouseDao
from app.utils.DBHelper import MyHelper
class Test1(unittest.TestCase):
    def test1(self):
        a=WareHouseDao()
        result = a.getAllInfo()
        print(result)