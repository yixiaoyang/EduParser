# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium

def handler(tag):
    tds = tag.find_all("td")
    if not tds or len(tds) != 4:
        return None
    employee = Employee()
    ass = tag.find_all('a')
    if ass and len(ass) != 0:
        employee.url = ass[0]['href']
    employee.name = tds[0].get_text().strip()
    employee.name = ''.join(employee.name.split())

    title = tds[1].get_text()
    if title and len(title) != 0:
        employee.title = ''.join(title.split())

    email = tds[3].get_text()
    if email and len(email) != 0:
        employee.email = ''.join(email.split())


    tel = tds[2].get_text()
    if tel and len(tel) != 0:
        employee.tel = ''.join(tel.split())

    return employee

def set_attr_hook(name,value):
    if name == 'departments':
        if len(value) > 32:
            return None
    elif name == 'email':
        pass
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", class_="rightb_con", limit=1)
    if not divs or len(divs) == 0:
        div = soup
    else:
        div = divs[0]

    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()

    return employee
