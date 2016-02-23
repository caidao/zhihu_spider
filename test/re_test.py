#coding:utf8

import re
from pybloom import BloomFilter
from pybloom.utils import range_fn

str = 'paner1223'

pat = re.compile(r'span')

ma =pat.match(str)



f = BloomFilter(capacity=10000, error_rate=0.001)
for i in range_fn(0, f.capacity):
    f.add(i)
print (9999 in f)

filepath = '../out/filter.txt'
bloom_one = BloomFilter(100, 0.001)
bloom_one.add('https://www.zhihu.com/people/tang-yun-44-97')
bloom_one.add('https://www.zhihu.com/people/tang-yun-44-98')
bloom_one.add('https://www.zhihu.com/people/tang-yun-44-18')
bloom_one.add('https://www.zhihu.com/people/tang-yun-44-38')
# f = open(filepath, 'w')
# bloom_one.tofile(f)

# f = open(filepath, 'r')
# bloom_new= BloomFilter.fromfile(f)
# bloom_new = BloomFilter(10, 0.001)
# bloom_two.add('test22')
# bloom_two.add('test33')
# bloom_new.add(bloom_two)

# f = open(filepath, 'w')
# bloom_new.tofile(f)
# f.close()
# print f
if 'https://www.zhihu.com/people/tang-yun-44-38' in bloom_one:
    print ('sus')