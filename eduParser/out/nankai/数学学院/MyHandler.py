# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    return Employee(name=tag.string.strip(), url=tag['href'])

def set_attr_hook(name,value):
    if name == 'departments':
        if len(value) > 32:
            return None
    elif name=='research':
        symbol = '社会兼职'
        if symbol in value:
            return '*'
    elif name == 'email':
        value = value.replace('at','@')
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    
    #div_header = soup.find_all(name="div", attrs={"class":"neiye-shizi-title"}, limit=1)
    
    divs = soup.find_all(name="div", attrs={"class":"xinwen-txt_3"}, limit=1)
    if not divs or len(divs) == 0:
        return employee

    div = divs[0]
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
    
    # 使用纯文本方式处理
    lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,ignore=set(['fax']))
    return parser.parse()
