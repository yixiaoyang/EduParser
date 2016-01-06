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
    name = tag.string or tag.get_text()
    name = ''.join(name.split())
    return Employee(name=tag.string,url=tag['href'])


def set_attr_hook(name,value):
    if name == 'email':
        if not '@' in value:
            return ''
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", class_="xq_teacher", limit=1)
    if not divs or len(divs) == 0:
        return employee

    div = divs[0]
    
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
        
    # 找到科研方向
    details = div.find_all("div",class_="con01_t",limit=3)
    if details and len(details) >= 2:
        employee.research = details[1].get_text()
        employee.research = ''.join(employee.research.split())
        # 过滤掉太短的串
        if len(employee.research) <= (len(u'研究方向')+1):
            employee.research = ''
        else:
            employee.research.replace(',','，')
    
    # 解析其他各人信息
    infos = div.find_all("div",class_="wz_teacher",limit=1)
    if infos and len(infos) != 0:
        # 使用纯文本方式处理
        lines = infos[0].stripped_strings
        parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,force_email=True)
        return parser.parse()
    else:
        return employee
