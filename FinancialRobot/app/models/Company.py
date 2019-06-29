#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class Company:
    def __init__(self,id,name,place):
        self.__id=id
        self.__name=name
        self.__place=place
    # __id                 #公司的编号
    # __name               #公司的名称
    # __place              #公司的地址
    def getId(self):
        return self.__id
    def setId(self,value):
        self.__id=value
    def getName(self):
        return self.__name
    def setName(self,value):
        self.__name=value
    def getPlace(self):
        return self.__place
    def setPlace(self, value):
        self.__place = value


