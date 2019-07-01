#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class Warehouse:
    def __init__(self, id, name, site, companyId):
        self.__name = name
        self.__position = site
        self.__ID = id
        self.__CompanyId = companyId

    def getCompanyId(self):
        return self.__CompanyId

    def setCompanyId(self, value):
        self.__CompanyId = value

    def getId(self):
        return self.__ID

    def setId(self, value):
        self.__ID = value

    def getName(self):
        return self.__name

    def setName(self, value):
        self.__name = value

    def getPosition(self):
        return self.__position

    def setPosition(self, value):
        self.__position = value
