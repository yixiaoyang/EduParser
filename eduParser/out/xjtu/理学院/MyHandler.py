# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium
import time

PROFILE_TITLES = [u'副教授', u'助理教授', u'教授', u'讲师', u'院长', u'副院长', u'高级工程师', u'工程师', u'院士', u'副研究员', u'研究员',u'高级实验师']

# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    return Employee(name=tag.string.strip(), url=tag['href'])

def set_attr_hook(name,value):
    if name == 'departments' or name == 'email':
        if len(value) > 64:
            return None
    elif name=='profile':
        return None
    elif name == 'title':
        if not value in PROFILE_TITLES:
            return None
    elif name == 'tel':
        if u'版本' in value:
            return None
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", clasS_="content-wrapper", limit=1)
    if not divs or len(divs) == 0:
        div = soup
    else:
        div = divs[0]
    
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()

    infos_div = div.find_all('div',attrs={"id":"column-1"})
    if infos_div and len(infos_div) != 0:
        div = infos_div[0]

    # 使用纯文本方式处理
    lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,max_line=256)
    return parser.parse()


