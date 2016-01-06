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
    if not tds or len(tds) != 6:
        print len(tds)
        return None

    name = tds[0].get_text().strip()
    name = ''.join(name.split())

    if name == u'姓名':
        return None

    title = tds[1].get_text()
    if title and len(title) != 0:
        title = title.strip()

    tel = tds[2].get_text()
    if tel and len(tel) != 0:
        tel = tel.strip()

    email = tds[3].get_text()
    if email and len(email) != 0:
        email = email.strip()
        if '@' in email:
            email = email + 'ustc.edu.cn'

    department = tds[5].get_text()
    if department and len(department) != 0:
        department = department.strip()

    url = ''
    ass = tds[0].find_all('a')
    if ass:
        url = ass[0]['href']
    return Employee(name=name, title=title, url=url, email=email, tel=tel, departments=department)

def set_attr_hook(name,value):
    if name == 'departments':
        if len(value) > 64:
            return None
    elif  name == 'email':
        if not '@' in value:
            return None
    elif name == 'title':
        value = value.replace('：','')
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"class":"ejcontent"}, limit=1)    
    if not divs or len(divs) == 0:
        print "not found main div"
        div = soup
    else:
        div = divs[0]
    
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()

    return employee


