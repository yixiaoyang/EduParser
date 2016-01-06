#!/usr/bin/python
# -*- coding: utf-8 *-*

from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import urllib2
import sys


doc = None
with open('index.html','rb') as fp:
    doc = fp.read()
    fp.close()

soup = BeautifulSoup(doc,"html.parser")
res = soup.find_all("a",attrs={"style":"FONT-SIZE: 12px; TEXT-DECORATION: underline"})
for e in  res:
    print e.text
    #print e