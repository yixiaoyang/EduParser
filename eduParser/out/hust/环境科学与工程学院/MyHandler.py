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
    tds = tag.find_all("td")
    if not tds or len(tds) < 4:
        return None
    name = tds[0].get_text()
    if u'姓名' in name:
        return None
    departments = tds[1].get_text()
    tel = tds[2].get_text()
    email = tds[3].get_text()
    ass = tag.find_all('a')
    url = ''
    if ass and len(ass) != 0:
        url = ass[0]['href']
    return Employee(name=name, tel=tel, email=email, url=url, departments = departments)

def set_attr_hook(name,value):
    if name == 'departments':
        if len(value) > 32:
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
    divs = soup.find_all(name="td", attrs={"height":"341"}, limit=1)
    if not divs or len(divs) == 0:
        div= soup
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
    parser = ProfileParser(lines=lines,employee=employee, max_line="999",force_email=True, force_tel=True)
    return parser.parse()
