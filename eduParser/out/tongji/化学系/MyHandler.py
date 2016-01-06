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
    name_symbol = u'姓名'
    tds = tag.find_all('td')
    
    if len(tds) != 7:
        return None
    if tds[0].get_text().strip() == name_symbol:
        return None
    employee = Employee()
    
    ass = tds[0].find_all('a')
    if len(ass) != 0:
        employee.url = ass[0]['href']
    employee.name = tds[0].get_text().strip()
    employee.email = tds[2].get_text().strip()
    employee.title = tds[3].get_text().strip()
    employee.research = tds[6].get_text().strip()
    employee.research.replace('\n','.')
    print employee.name,employee.email,employee.title
    return employee


# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"class":"con_nr"}, limit=1)
    if not divs or len(divs) == 0:
        return employee

    div = divs[0]
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
    
    return employee
