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
    tds = tag.find_all(name='td')
    if not tds:
        print("len(tds) == 0")
        return None

    employee = Employee()
    if len(tds) < 5:
        print("len(tds) = %d"%(len(tds)))
        return None

    name_tag = None
    name_tag_idx = 0
    if len(tds) == 5:
        name_tag_idx = 0
        name_tag = tds[name_tag_idx]
    elif len(tds) > 5:
        name_tag_idx = 1
        name_tag = tds[name_tag_idx]

    employee.name = name_tag.get_text()
    employee.name = employee.name.strip()
    if employee.name == u'姓名':
        return None
    ass = name_tag.find_all('a')
    if ass and len(ass) != 0:
        employee.url = ass[0]['href']
    
    employee.title = tds[name_tag_idx+1].get_text().strip()
    employee.email = tds[name_tag_idx+2].get_text().strip()
    employee.tel   = tds[name_tag_idx+3].get_text().strip()

    return employee

def set_attr_hook(name,value):
    if name == 'departments':
        if len(value) > 32:
            return None
    elif name == 'email':
        if not '@' in value:
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
    divs = soup.find_all(name="div", attrs={"class":"Article_Content"}, limit=1)
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
    # ,set_attr_hook=set_attr_hook
    parser = ProfileParser(lines=lines,employee=employee)
    return parser.parse()
