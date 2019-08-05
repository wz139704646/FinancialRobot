#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime


class timeProcess:
    @classmethod
    def get_last_month(self, d):
        dayscount = datetime.timedelta(days=d.isoweekday())
        dayto = d - dayscount
        sixdays = datetime.timedelta(days=6)
        dayfrom = dayto - sixdays
        date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
        date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
        return date_from

    @classmethod
    def get_current_month(self, d):
        dayscount = datetime.timedelta(days=d.day)
        dayto = d - dayscount
        date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
        date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
        print
        '---'.join([str(date_from), str(date_to)])
        return date_from

    @classmethod
    def get_current_week(self, day):
        monday, sunday = day, day
        one_day = datetime.timedelta(days=1)
        while monday.weekday() != 0:
            monday -= one_day
        while sunday.weekday() != 6:
            sunday += one_day
        # 返回当前的星期一和星期天的日期
        return monday
