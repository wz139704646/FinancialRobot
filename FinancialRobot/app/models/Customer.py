#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class Customer():
    # __ID         #顾客编号（也可为身份证
    # __name       #顾客名称
    # __phone      #顾客电话
    # __credit     #顾客信誉信息 从花旗API获得
    # __companyId  #顾客所属公司 从登陆信息获得

    def __init__(self, id, name, phone, companyId):
        self.__ID = id
        self.__name = name
        self.__phone = phone
        self.__companyId = companyId

    def getId(self):
        return self.__ID

    def setId(self, value):
        self.__ID = value

    def getName(self):
        return self.__name

    def setName(self, value):
        self.__name = value

    def getPhone(self):
        return self.__phone

    def setPhone(self, value):
        self.__phone = value

    def getCredit(self):
        return self.__credit

    def setCredit(self, value):
        self.__credit = value

    def getCompanyId(self):
        return self.__companyId

    def setCompanyId(self, value):
        self.__companyId = value
