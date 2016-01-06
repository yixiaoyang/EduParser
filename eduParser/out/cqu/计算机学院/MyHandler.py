# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium
import time


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    name_div = tag.find_all('span',class_='name')
    zc_div = tag.find_all('span',class_='zc')
    lxfs_div = tag.find_all('span',class_='lxfs')
    research_div = tag.find_all('span',class_='major')
    
    name = name_div[0].get_text()
    title = zc_div[0].get_text()
    email = lxfs_div[0].get_text()
    research = research_div[0].get_text()

    name = name.strip()
    if not name or len(name) == 0:
        return None
    name = ''.join(name.split())
    if title and len(title) != 0:
        title = title.strip()
    if email and len(email) != 0:
        email = email.strip()
        emails = email.split(' ')
        email = emails[0]
        email = email.replace('(at)','@')
        if not '@' in email:
            email = email + '@cqu.edu.cn'
    if research and len(research) != 0:
        research = research.strip()

    return Employee(name=name, email=email, title=title, research=research)


