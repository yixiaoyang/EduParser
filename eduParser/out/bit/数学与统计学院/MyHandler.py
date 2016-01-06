# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium

PROFILE_TITLES = set([u'副教授', u'助理教授', u'教授', u'讲师', u'院长', u'副院长', u'工程师', u'院士', u'副研究员', u'研究员'])


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    name = tag.string or tag.get_text()
    name = ''.join(name.split())
    return Employee(name=tag.string,url=tag['href'])



# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", class_="box_rt01 list", limit=1)
    if not divs or len(divs) == 0:
        div = soup
    else:
        div = divs[0]

    with open(filename, 'wb') as fp:
        content = div.prettify()
        fp.write(content)
        fp.close()

    h3s = div.find_all('h3')
    if h3s and len(h3s) != 0:
        title = h3s[0].get_text()
        title = ''.join(title.split())
        print title
        for t in PROFILE_TITLES:
            if t in title:
                employee.title = title
                print "got => " + title
                break
    else:
        print "not found h3"
    # 使用纯文本方式处理
    lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,force_email=True)
    return parser.parse()
