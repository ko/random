#!/usr/bin/python2.7

import time

def follow(target):
    target.seek(0,2)    # go to EOF
    while True:
        line = target.readline()
        if not line:
            time.sleep(0.1) # brief
            continue
        yield line

# similar result as `tail -f`
def example():
    logfile = open("access-log")
    loglines = follow(logfile)

    for line in loglines:
        print line


