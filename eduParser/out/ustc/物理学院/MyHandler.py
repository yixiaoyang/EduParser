# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium
import re

l_departments = None

# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    global l_departments
    tds = tag.find_all(name='td')

    print tag
    print len(tds)
    if not tds or len(tds) < 7:
        return None

    start = 1 if len(tds) == 7 else 2
    if len(tds) > 7:
        l_departments = tds[1].get_text()

    name = tds[start+0].get_text().strip()
    name = ''.join(name.split())

    research = tds[start+2].get_text().strip() or ''
    research = research.replace(',','，')


    tel = tds[start+3].get_text() or ''
    tel = tel.strip()


    email = tds[start+4].get_text() or ''
    email = email.strip()


    url = ''
    ass = tds[start].find_all('a')
    if ass:
        url = ass[0]['href']

    return Employee(name=name, url=url, email=email, tel=tel, research=research, departments=l_departments or '')
