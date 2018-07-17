#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 14:22
# @Author  : Py.qi
# @File    : test1.py
# @Software: PyCharm
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
cookies='JSESSIONID=ADEF57C7D042001F2C7423F2D81A23B7; tk=vYceFnEJy9UYYfV_SbnM4AiE6qyATtSyL8V0NYKdMMMcgz2z0; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=434373130.64545.0000; BIGipServerpool_passport=200081930.50215.0000; RAIL_EXPIRATION=1532032610521; RAIL_DEVICEID=JDvPVlxJmlRmPEOHHLTO40DtNoSLPLIN1JkOVpXMR_V1upBNsQHJHsu3QsnmVzrCigNvnn7v-lOy5biKzkBtrPbyx1OhRIMCsCl5MXMrTA5LGVpetd8SZieJokmxebdnjI76XnTg3VDinMIvBlOGwTIoZlLt9oxx; current_captcha_type=Z; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2018-07-16; _jc_save_toDate=2018-07-16; _jc_save_wfdc_flag=dc'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

jar=RequestsCookieJar()
for i in cookies.split(';'):
    key,value=i.split('=',1)
    jar.set(key,value)

r=requests.get('https://kyfw.12306.cn/otn/leftTicket/init',cookies=jar,headers=headers)
print(r.request.headers['Cookie'])
print(r.status_code)
print(r.text)