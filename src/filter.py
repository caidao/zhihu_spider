#coding:utf8

from pybloom import BloomFilter

class Filter(object):
    def __init__(self, bloom_from_sql):
        self.bloom_cache = bloom_from_sql
        self.count=0

    def check(self, url):
        #如果url在缓存过滤器中，直接返回true
        if url in self.bloom_cache:
            return True
        else:
            self.count+=1
            self.bloom_cache.add(url)

        return False

    def _tofile_(self):
        #没增加1000个url就保存一次过滤器
        if self.count % 1000==0:
            f = open('../out/filter', 'w')
            self.bloom_cache.tofile(f)
            f.close()
            print "重复url="+self.count

    def _fromfile_(self):
        try:
            f= open('../out/filter', 'r')
            self.bloom_cache=BloomFilter.fromfile(f)
            self.count=self.bloom_cache.count
            f.close()
        except Exception, ex:
            print(Exception, ex)
            self.bloom_cache = BloomFilter(capacity=10000000, error_rate=0.00001)
            self.count=0




