#!/usr/bin/python
# -*- coding:utf8 -*-

import urllib2
import re

url = urllib2.urlopen("http://txt.go.sohu.com/ip/soip")
text = url.read()
ip = re.findall(r'\d+.\d+.\d+.\d+',text)

print ip[0]

#

#curl -s http://txt.go.sohu.com/ip/soip  | awk '{t=$0;gsub(/.*sohu_user_ip="|";.*/,"",t);print t}'
#https://kinggoo.com/ob-ip.htm

