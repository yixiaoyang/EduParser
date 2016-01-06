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
    name = tag.get_text()
    if not name:
        return None
    name = ''.join(name.split())
    name = name.replace('*','')
    name = name.replace('﹡','')
    name = name.replace('※','')
    
    ass = tag.find_all('a')
    url = ass[0]['href'] if len(ass) != 0 else ''
    
    return Employee(name=name, url=url)

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
    divs = soup.find_all(name="div", attrs={"class":"darea"}, limit=1)
    if not divs or len(divs) == 0:
        return employee

    div = divs[0]
    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()
    
    dnodes = div.find_all(name='div',class_=u"dnode")
    if not dnodes or len(dnodes) == 0:
        return employee
    
    lines = None
    target_node = None
    done = False
    for node in dnodes:
        lines = node.stripped_strings
        for count,line in enumerate(lines):
            if count >= 2:
                break;
            if line == u'联系方式':
                print "binggo!"
                target_node = node
                done = True
                break
        if done:
            break
    
    if not target_node:
        return employee
    
    lines = []
    trs = node.find_all('tr')
    if trs and len(trs) != 0:
        for tr in trs:
            text = tr.get_text()
            if text:
                text = ''.join(text.split())
                lines.append(text)
    else:
        lines = node.stripped_strings
    #lines = target_node.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook)
    return parser.parse()
