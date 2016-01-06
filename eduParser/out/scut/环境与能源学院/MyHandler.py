# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium

from config import Config

def handler(tag):
    name = tag.get_text()
    name = ''.join(name.split())
    name = name.replace('（','(')
    title = ''
    for t in Config.PROFILE_TITLES:
        if t in name:
            name = name.replace(t,'')
            title = t
            break
    return Employee(name=name, url=tag['href'], title = title)

def set_attr_hook(name,value):
    if name == 'email':
        if not u'@' in value:
            return None
    return value


def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"class":"content"}, limit=1)
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
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook, max_line="999",
        force_email=True, force_tel=False, ignore=set(['fax','departments']))
    return parser.parse()
