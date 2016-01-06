#!/usr/bin/python
# -*- coding: utf-8 *-*

from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import urllib2
import sys

doc = None
with open('ΩÃ ¶11.html','rb') as fp:
	doc = fp.read()
	fp.close()

soup = BeautifulSoup(doc,"html.parser")
res = soup.find_all("div", class_="pane-content")

for i, r in enumerate(res):
    print r
print (len(res))