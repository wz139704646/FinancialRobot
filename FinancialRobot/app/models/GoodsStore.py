#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class GoodsStore():
    # # 商品存储表：以商品编号、仓库编号和公司编号共同作为表的主键
    # __goodsId
    # __companyId
    # __wareId
    # __number      #货物存储数量
    def __init__(self, gid ,cId,wid,number):
        self.__goodsId = gid
        self.__companyId=cId
        self.__wareId = wid
        self.__number = number
    def getGoodsId(self):
        return self.__goodsId
    def setGoodsId(self, value):
        self.__goodsId = value

    def getCompanyId(self):
        return self.__companyId
    def setCompanyId(self, value):
        self.__companyId = value

    def getWareId(self):
        return self.__wareId
    def setWareId(self, value):
        self.__wareId = value

    def getNumber(self):
        return self.__number
    def setNumber(self, value):
        self.__number = value