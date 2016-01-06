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
    email_tail = '@ustc.edu.cn'
    tel_pre = '0551-360'

    tds = tag.find_all(name='li')
    if not tds or len(tds) < 4:
        return None

    print tag
    name = tds[0].get_text().strip()
    name = ''.join(name.split())

    title = tds[1].get_text().strip()
    
    tel = tds[3].get_text().strip()
    tel = tel_pre+tel


    email = tds[2].get_text() or ''
    email = email.strip()
    email = email+email_tail

    url = ''
    ass = tds[0].find_all('a')
    if ass:
        url = ass[0]['href']

    return Employee(name=name, url=url, email=email, tel=tel, title=title)


# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"class":"post"}, limit=1)
    if not divs or len(divs) == 0:
        print("main div not found")
        return employee

    div = divs[0]
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
    
    return employee
