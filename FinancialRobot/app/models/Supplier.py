#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class Supplier:
    def __init__(self, _id, name, phone, site):
        self.__id = _id
        self.__name = name
        self.__phone = phone
        self.__site = site

    def getId(self):
        return self.__id

    def setId(self, value):
        self.__id = value

    def getName(self):
        return self.__name

    def setName(self, value):
        self.__name = value

    def getPhone(self):
        return self.__phone

    def setPhone(self, value):
        self.__phone = value

    def getSite(self):
        return self.__site

    def setSite(self, value):
        self.__site = value
