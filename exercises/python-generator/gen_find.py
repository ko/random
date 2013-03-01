#!/usr/bin/python2.7

import os
import fnmatch

def gen_find(filepath, root):
    for path, dirlist, filelist in os.walk(root):
        for name in fnmatch.filter(filelist, filepath):
            yield os.path.join(path, name)


pyfiles = gen_find("*.py", "/home/ko")
for pf in pyfiles:
    print pf
