# coding=utf-8
import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser
from mparser import get_doc_bySelenium
import time


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    return Employee(name=tag.string.strip(), url=tag['href'])

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
    divs = soup.find_all(name="table", attrs={"width":"772"}, limit=1)
    if not divs or len(divs) == 0:
        div = soup
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
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook)
    return parser.parse()

# img3,4,5 div=imgimg11
def engine_handler_test(driver):
    doc = None
    try:
        link = driver.find_element_by_id(u'img3')
        if link:
            link.click()
        link = driver.find_element_by_id(u'img4')
        if link:
            link.click()
        link = driver.find_element_by_id(u'img5')
        if link:
            link.click()
        link = driver.find_element_by_id(u'img111')
        if link:
            link.click()
        
        time.sleep(0.5)
        doc = driver.page_source
    except Exception as e:
        return doc
    return doc
