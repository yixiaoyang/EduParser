# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium,get_doc_byUrllib2
import re
from urlparse import urlparse, urljoin

# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    name = tag.get_text().strip()
    url = tag['href']
    return Employee(name=name, url=url)

def set_attr_hook(name,value):
    if name == 'departments':
        if len(value) > 64:
            return None
    elif name == 'email':
        if len(value) > 64:
            return None
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
    
    lis = soup.find_all(name="li")
    if not lis and len(lis) != 5:
        div = soup
    else:
        ass = lis[4].find_all('a')
        if len(ass) != 0:
            li_url = ass[0]['href']
            newUrl = urljoin(url,li_url)
            newDoc = get_doc_byUrllib2(newUrl)
            soup = BeautifulSoup(newDoc, Config.SOUP_PARSER)
            mainDiv = soup.find_all('div',attrs={"id":"main"})

            if not mainDiv or len(mainDiv) == 0:
                print "not found main div"
                div = soup
            else:
                div = mainDiv[0]

    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()

    # 使用纯文本方式处理
    lines = div.stripped_strings
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,force_email=True)
    return parser.parse()


