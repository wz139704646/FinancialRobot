#!/usr/bin/env python 
# -*- coding:utf-8 -*-

class sell:
    def __init__(self, cid, gid, number, uprice, sprice, date):
        self.__customerId = cid
        self.__goodsId = gid
        self.__number = number
        self.__unitPrice = uprice
        self.__sumPrice = sprice
        self.__date = date

    def getCustomerId(self):
        return self.__customerId

    def setCustomerId(self, value):
        self.__customerId = value

    def getGoodsId(self):
        return self.__goodsId

    def setGoodsId(self, value):
        self.__goodsId = value

    def getNumber(self):
        return self.__number

    def setNumber(self, value):
        self.__number = value

    def getDate(self):
        return self.__date

    def setDate(self, value):
        self.__date = value

    def getUnitprice(self):
        return self.__unitPrice

    def setUnitprice(self, value):
        self.__unitPrice = value

    def getSumprice(self):
        return self.__sumPrice

    def setSumprice(self, value):
        self.__sumPrice = value
