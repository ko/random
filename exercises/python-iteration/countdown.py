#!/usr/bin/python2.7

class countdown(object):
    def __init__(self, start):
        self.count = start
    def __iter__(self):
        return self
    def next(self):
        if self.count <= -1:
            raise StopIteration
        r = self.count
        self.count -= 1
        return r

for x in countdown(10):
    print x
