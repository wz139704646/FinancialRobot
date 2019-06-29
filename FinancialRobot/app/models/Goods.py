#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class Goods():
    # 商品编号和公司编号一起作为商品的主键 不同公司的商品编号可能一致
    # __id
    # __companyId
    # __name       #商品名称
    # __sellprice  #商品售价 与进货表中的进价想减得出利润
    # __number     #商品剩余数量
    def __init__(self, id, name, companyId, sprice, number):
        self.__id = id
        self.__name = name
        self.__companyId = companyId
        self.__sellprice = sprice
        self.__number = number

    def getId(self):
        return self.__id

    def setId(self, value):
        self.__id = value

    def getName(self):
        return self.__name

    def setName(self, value):
        self.__name = value

    def getSellPrice(self):
        return self.__sellprice

    def setSellPrice(self, value):
        self.__sellprice = value

    def getCompanyId(self):
        return self.__companyId

    def setCompanyId(self, value):
        self.__companyId = value

    def getNumber(self):
        return self.__number

    def setNumber(self, value):
        self.__number = value
