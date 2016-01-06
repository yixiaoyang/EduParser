# coding=utf-8

import os
from models import Employee
from bs4 import BeautifulSoup
from config import Config
from mparser import ProfileParser, dl_byUrllib2

from PIL import Image
import subprocess
import pytesseract

from image_magic_sh import image_resize,image_mono

#姓名  研究方向    联系邮箱    办公地址
# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    name = tag.get_text()
    url = tag['href']
    name = ''.join(name.split())
    name = name.strip()
    return Employee(name=name, url=url)

def set_attr_hook(name,value):
    return value

def imageSrc(tag):
    imgs = tag.find_all('img')
    if imgs and len(imgs) > 0:
        return imgs[0]['src']
    return None

def image2text(url, filename,lang):
    if not url:
        return ''
    if not os.path.exists(filename):
        dl_byUrllib2(url,filename)
        image_resize(filename,filename)
        image_mono(filename,filename)

    image_fp = Image.open(filename)
    string = pytesseract.image_to_string(image_fp,lang=lang)
    return string
        
# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    email_image_filename = os.path.join(path, name  + "_email.png")
    tel_image_filename = os.path.join(path, name  + "_tel.png")

    employee = Employee(name=name, url=url)
    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", attrs={"id":"view_pannel"}, limit=1)
    if not divs or len(divs) == 0:
        div = soup
    else:
        div = divs[0]

    if not os.path.exists(filename):
        with open(filename, 'wb') as fp:
            content = div.prettify()
            fp.write(content)
            fp.close()

    # email image 
    item_divs = div.find_all(name="div", attrs={"class":"item_list"})

    ignores =[]
    for div in item_divs:
        string = div.get_text()
        if string and len(string) != 0:
            if u'邮件' in string and len(employee.email) == 0:
                employee.email = image2text(imageSrc(div),email_image_filename,'eng2')
                print(employee.email)
                ignores.append('email')
            elif u'电话' in string  and len(employee.tel) == 0:
                employee.tel = image2text(imageSrc(div),tel_image_filename,'eng')
                print(employee.tel)
                ignores.append('tel')

    # 使用纯文本方式处理
    lines = div.stripped_strings
    # text=div.get_text(strip=True)
    parser = ProfileParser(lines=lines,employee=employee,set_attr_hook=set_attr_hook,max_line=256,ignore=set(ignores))
    return parser.parse()
