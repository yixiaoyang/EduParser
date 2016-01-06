#!/usr/bin/python
# -*- coding: utf-8 *-*

from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import urllib2
import sys


doc = None
with open('tjdx.htm','rb') as fp:
	doc = fp.read()
	fp.close()

soup = BeautifulSoup(doc,"html.parser")
print soup.title.string