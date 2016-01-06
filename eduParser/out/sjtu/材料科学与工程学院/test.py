#!/usr/bin/python
# -*- coding: utf-8 *-*

from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import urllib2
import sys


doc = None
with open('金朝晖.html','rb') as fp:
    doc = fp.read()
    fp.close()

soup = BeautifulSoup(doc,"html.parser")
#soup = BeautifulSoup(doc,"lxml")
researches = [' ',' ']
tds = soup.find_all(name="td",attrs={"bgcolor":"#FFFFFF","class":"ft12","valign":"top"},limit=4)
print tds

for i, td in enumerate(tds):
    print i, td