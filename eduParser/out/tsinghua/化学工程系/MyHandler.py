# coding=utf-8

from models import Employee
from bs4 import BeautifulSoup
from config import Config


# @brief: 函数将过滤结果转化为Employee数据
# @tag: 输入为待处理的BeautifulSoup的tag对象
# @output:输出employee
def handler(tag):
    employee = Employee(url=tag['href'], name=tag.string)
    #print(tag)
    return employee


# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None

'''
蒋国强
副教授
研究方向：药物传输工程和控释技术、化学与生物反应工程
    办公电话： (O)86-10-62782824 (L)86-10-62773845
    办公地址：北京清华大学英士楼4层 化学工程系 生物化工研究所
    电子邮件： jianggq@tsinghua.edu.cn

<td valign="top">
<h3>蒋国强 </h3>
<dl>
<dt>副教授</dt>
<dt>研究方向：药物传输工程和控释技术、化学与生物反应工程</dt>
<dd>办公电话： (O)86-10-62782824  (L)86-10-62773845</dd>
<dd>办公地址：北京清华大学英士楼4层 化学工程系 生物化工研究所</dd>
<dd>电子邮件： jianggq@tsinghua.edu.cn</dd>
</dl>
</td>

<div class="teachcontent"><p><a href="http://www.chemeng.tsinghua.edu.cn/scholars/jianggq/indexsc.html"><span style="color: rgb(0, 0, 255);"><u><strong>个人主页地址</strong></u></span></a></p>
</div>
'''
# @doc: 输入为个人详情页的整个网页源码
# @output:输出employee，如果没有检测到内容返回None          
# employee可用属性(url, name, email, tel, title, profile, research, departments,fax,addr):
def profile_handler(doc, name, url, path):
    filename = os.path.join(path, name + ".html")
    employee = Employee(name=name, url=url)

    # 只保存名称和个人主页，个人简历文件另存当前目录
    soup = BeautifulSoup(doc, Config.SOUP_PARSER)
    divs = soup.find_all(name="div", class_="s2_right_con", limit=1)
    if not divs or len(divs) == 0:
        print("can't find div???")
        div = soup
        #return employee
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