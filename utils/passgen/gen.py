#!/usr/local/bin/python2.7
import argparse
import getpass
import os
import random

def read_key():
    keypath = os.getenv('HOME') + '/.ssh/id_rsa'
    lines = [line.strip() for line in open(keypath)]
    start = 0; end = 0
    for k,v in enumerate(lines):
        if v == '-----BEGIN RSA PRIVATE KEY-----':
            start = k+1
        elif v == '-----END RSA PRIVATE KEY-----':
            end = k-1
            break
    return {
                'lines': lines,
                'start': start,
                'end': end,
            }

def get_params():
    hostname = raw_input("hostname: ")
    username = raw_input("username: ")
    passphrase = getpass.getpass('passphrase: ')

    retry = True
    while retry:
        p1 = getpass.getpass('[verify]: ')
        if passphrase == p1:
            retry = False
        elif passphrase != p1:
            retry = True
            passphrase = getpass.getpass('passphrase: ')

    params = {
                'hostname': hostname,
                'user': username,
                'pass': passphrase,
            }
    return params

def generate(params, k, passlength=16):
    s = ''
    ascii_min = 32  # space
    ascii_max = 126 # backtick? something visible before ^H
    """
    h = params['hostname'] 
    u = params['user']
    p = params['pass']
    print '{0},{1},{2}'.format(h,u,p)
    """ 
    for i in range(0,passlength):
        lineno = k['end'] % passlength
        random.seed(k['lines'][lineno][i])
        val = random.randint(ascii_min, ascii_max) 
        s += chr(val)

    print '--->[' + s + ']<---'

k = read_key()
p = 1
#p = get_params()
generate(p,k,16)

