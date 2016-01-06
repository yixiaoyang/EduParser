# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium
import re


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    tds = tag.find_all(name='td')
    if not tds or len(tds) < 5:
        return None

    department = tds[0].get_text()
    if not department or len(department) == 0:
        return None
    department = department.strip()
    
    name = tds[1].get_text().strip()
    name = ''.join(name.split())

    url = ''
    ass = tds[1].find_all('a')
    if ass:
        url = ass[0]['href']

    title = tds[2].get_text() or ''
    title = title.strip()

    email = ''
    research = ''
    tel = ''
    if len(tds) == 5:
        email = tds[3].get_text() or ''
        email = email.strip()

        tel = tds[4].get_text() or ''
        tel = tel.strip()
    elif len(tds) == 6:
        research = tds[3].get_text() or ''
        research = research.strip()

        email = tds[4].get_text() or ''
        email = email.strip()

        tel = tds[5].get_text() or ''
        tel = tel.strip()

    return Employee(name=name, email=email, tel=tel, research = research, departments=department)
