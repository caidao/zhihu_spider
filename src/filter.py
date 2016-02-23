#coding:utf8

from pybloom import BloomFilter

class Filter(object):
    def __init__(self):
        self.bloom_cache = BloomFilter(capacity=10000000, error_rate=0.00001)
        self.temp = list()
        self.count=0

    def check(self, url):
        #如果url在缓存过滤器中，直接返回true
        if url in self.bloom_cache:
            self.count+=1
            return True
        else:
            self.bloom_cache.add(url)
            self.temp.append(url)

        return False

    def __del__(self):
        self.file = open('../out/filter', 'w')
        self.bloom_cache.tofile(self.file)
        print "重复url="+self.count
        del self.bloom_cache



