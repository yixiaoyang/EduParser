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
    tds = tag.find_all(name='td',class_="dh01")
    if not tds or len(tds) != 4:
        return None
    name = tds[0].get_text().strip()
    name = ''.join(name.split())

    department = tds[1].get_text()
    if not department or len(department) == 0:
        return None

    email = tds[2].get_text() or ''
    email = email.strip()

    tel = tds[3].get_text() or ''
    tel = tel.strip()

    url = ''
    ass = tds[0].find_all('a')
    if ass:
        url = ass[0]['href']
    return Employee(name=name, url=url, email=email, tel=tel, departments=department)

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
    divs = soup.find_all(name="table", attrs={"width":"96%","cellspacing":"0"}, limit=1)    
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

    divs = soup.find_all(name="table", attrs={"width":"96%","cellspacing":"1"}, limit=1)
    if not divs or len(divs) == 0:
        print "not found main div"
        div = soup
    else:
        div = divs[0]

    ass = div.find_all('a',text="点击此处访问")
    if ass and len(ass) != 0:
        employee.profile = ass[0]['href']
        print 'Got profile:' + employee.profile

    # 使用纯文本方式处理
    lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,max_line=256)
    return parser.parse()


