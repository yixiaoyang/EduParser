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
    name = tag.string.strip()
    return Employee(name=name, url=tag['href'])

def set_attr_hook(name,value):
    if name == 'departments' or name == 'email':
        if len(value) > 64:
            return None
    elif name == 'title':
        value = value.replace('：','')
    elif name == 'tel':
        value = value.replace('意见建议','')
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"id":"Tbody"}, limit=1)
    
    if not divs or len(divs) == 0:
        divs = soup.find_all(name="div", class_="peo_con", limit=1)
        if not divs or len(divs) == 0:
            div = soup
        else:
            div = divs[0]
    else:
        div = divs[0]
    
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
    
    # 使用纯文本方式处理
    lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,max_line=256)
    return parser.parse()


