# coding=utf-8

import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser

#姓名  研究方向    联系邮箱    办公地址
# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    tds = tag.find_all('td')
    if not tds or len(tds) != 4:
        return
    ass = tag.find_all('a') 
    name = tds[0].get_text()
    research = tds[1].get_text()
    email = tds[2].get_text()
    url = ass[0]['href'] if (ass and len(ass) > 0) else ''

    research = research.replace(',','，')
    research = research.strip()
    name = ''.join(name.split())
    name = name.strip()
    email = ''.join(email.split())
    email = email.strip()
    return Employee(name=name, email=email, url=url, research=research)

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"class":"bodyRight"}, limit=1)
    if not divs or len(divs) == 0:
        return employee

    div = divs[0]
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
    return employee
