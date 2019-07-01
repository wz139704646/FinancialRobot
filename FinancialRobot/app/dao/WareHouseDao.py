#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper
class WareHouseDao:
    def getAllInfo(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Warehouse")