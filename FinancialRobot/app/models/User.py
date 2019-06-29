#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class User:
    def __init__(self, account, password, id, phone, position):
        self.__account = account
        self.__password = password
        self.__phone = phone
        self.__position = position
        self.__ID = id

    def getId(self):
        return self.__ID

    def setId(self, value):
        self.__ID = value

    def getAccount(self):
        return self.__account

    def setAccount(self, value):
        self.__account = value

    def getPhone(self):
        return self.__phone

    def setPhone(self, value):
        self.__phone = value

    def getPosition(self):
        return self.__position

    def setPosition(self, value):
        self.__position = value

    def getPassword(self):
        return self.__password

    def setPassword(self, value):
        self.__password = value

    def getCompanyId(self):
        return self.__companyId

    def setCompanyId(self, value):
        self.__companyId = value
