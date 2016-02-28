#/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time

class MyThread(threading.Thread):
    """
    属性:
    target: 传入外部函数, 用户线程调用
    args: 函数参数
    """
    def __init__(self, target, args):
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.target = target
        self.args = args

    def run(self):
        self.target(self.args)

def print_time(counter):
    while counter:
        print "counter = %d" % counter
        counter -= 1
        time.sleep(1)



def main():
    my_thread = MyThread(print_time, 10)
    my_thread2 = MyThread(print_time, 10)
    my_thread2.start()
    my_thread.start()
    my_thread.join()
    my_thread2.join()

if __name__ == '__main__':
    main()