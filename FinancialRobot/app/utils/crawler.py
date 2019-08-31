#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import re

def helper(string, we_want):
    if we_want == '唯一一个小数':
        # 用来提取字符串中的唯一一个小数，局限性在于99,897,100这样的数字识别不了
        return re.search("-?\d+(\.\d+)?", string).group()
    elif we_want == '所有汉字':
        # 汉字的范围为”\u4e00-\u9fa5“，这个是用Unicode表示的
        return ''.join(re.findall('[\u4e00-\u9fa5]', string))
    return '这不科学'

def getValues():
    urlpage = 'http://quotes.money.163.com/f10/hydb_000001.html'
    print(urlpage)
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')
    temp = soup.find_all('tr')
    table = temp[5:10]
    PingAnBankData = soup.find_all('tr', "dbrow tr_hover")[0]
    table.append(PingAnBankData)
    print(temp[11])
    # temp[11] = temp[11].replace("\n", "")
    table.append(temp[11])
    print(temp[11])
    print('table')
    print(table)
    find_pe = lambda x: re.findall(r'<td class="sort_current">-?\d+\.?\d*</td>', str(x))
    find_pb_pcf = lambda x: re.findall(r'<td class="">-?\d+\.?\d*</td>', str(x))
    find_ps = lambda x: re.findall(r'<td class="td_last">-?\d+\.?\d*</td>', str(x))
    find_all_float = lambda x: re.findall(r"-?\d+\.?\d*", str(x))
    tup_num = []
    for string in table:
        if '<td class="align_c">行业平均</td>' in str(string):
            print('行业平均来了')
            print(string)
            pe = find_all_float(find_pe(string))[0]
            print('pe')
            print(pe)
            pb = find_all_float(find_pb_pcf(string)[0])[0]
            print('pb')
            print(pb)
            pcf = find_all_float(find_pb_pcf(string)[1])[0]
            print('pcf')
            print(pcf)
            ps = find_all_float(find_pb_pcf(string)[2])[0]
            print('ps')
            print(ps)
            tup_num.append(tuple([pe, pb, pcf, ps]))
            print(tup_num)
            return tup_num
        print(string)
        pe = find_all_float(find_pe(string))[0]
        print('pe')
        print(pe)
        pb = find_all_float(find_pb_pcf(string)[0])[0]
        print('pb')
        print(pb)
        pcf = find_all_float(find_pb_pcf(string)[1])[0]
        print('pcf')
        print(pcf)
        ps = find_all_float(find_ps(string))[0]
        print('ps')
        print(ps)
        tup_num.append(tuple([pe, pb, pcf, ps]))
        print(tup_num)
    return tup_num

def getCompanyNames():
    urlpage = 'http://quotes.money.163.com/f10/hydb_000001.html'
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')
    strs = []
    allstrs = soup.find_all("td", "align_c")[0:7]
    for string in allstrs[:-2]:
        strs.append(string)
    strs.append(allstrs[len(allstrs)-2])
    strs.append(allstrs[len(allstrs)-1])
    names = [helper(str(e), '所有汉字') for e in strs]
    return names


