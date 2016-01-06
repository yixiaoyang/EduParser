# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    name = tag.get_text()
    name = ''.join(name.split())
    names = name.split('_')
    name = names[0]
    employee = Employee(url=tag['href'], name=name)
    if len(names) >= 2:
        employee.title = names[1]
    return employee

def profile_set_attr_hook(name,value):
    if name == 'email':
        value = value.replace('AT','at')
        value = value.replace('(at)','@')
        value = value.replace('（at）','@')
        value = value.replace('@.','@')
    return value

# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="td",attrs={"valign":"center"}, limit=1)
    if not divs or len(divs) == 0:
        div = soup
    else:
        div = divs[0]
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()

    lines = []
    tds = div.find_all('td')
    if len(tds) == 0:
        lines = div.stripped_strings
        print "TDS none!"
    else:
        for td in tds:
            string = td.get_text().strip()
            if len(string) < 128:
                string = ''.join(string.split())
                print string
                lines.append(string)

    # 使用纯文本方式处理
    #lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=profile_set_attr_hook,max_line=256)
    return parser.parse()
