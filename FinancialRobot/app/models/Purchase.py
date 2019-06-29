#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class Purchase:
    # 进货表：以商品编号、公司编号和进货商编号共同作为表的主键
    # __goodId
    # __companyId
    # __supplierId
    # __number         #进货数量
    # __purchasePrice

    def __init__(self, gid ,cId,sid,number,pPrice):
        self.__goodsId = gid
        self.__companyId=cId
        self.__supplierId = wid
        self.__number = number
        self.__purchasePrice = pPrice

    def getGoodsId(self):
        return self.__goodsId
    def setGoodsId(self, value):
        self.__goodsId = value
    def getCompanyId(self):
        return self.__companyId
    def setCompanyId(self, value):
        self.__companyId = value
    def getSupplierId(self):
        return self.__supplierId
    def setSupplierId(self, value):
        self.__supplierId = value
    def getNumber(self):
        return self.__number
    def setNumber(self, value):
        self.__number = value
    def getpurchasePrice(self):
        return self.__purchasePrice
    def setpurchasePrice(self, value):
        self.__purchasePrice = value
