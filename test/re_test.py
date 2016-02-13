#coding:utf8

import re

str = 'paner1223'

pat = re.compile(r'span')

ma =pat.match(str)

print ma.group()