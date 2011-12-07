#!/usr/local/bin/python2.7
import argparse
import getpass
import os
import random

def read_key():
    keypath = os.getenv('HOME') + '/.ssh/id_rsa.pub'
    with open(keypath,'rb') as f:
        for line in f: print line

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

def generate(params, k):
    s = ''
    """
    h = params['hostname'] 
    u = params['user']
    p = params['pass']
    print '{0},{1},{2}'.format(h,u,p)
    """ 
    for i in range(0,16):
        # seed should be i'th char in the private key irl
        random.seed(i)
        val = random.randint(32,126) 
        s += chr(val)

    print '\"' + s + '\"'

"""
k = read_key()
p = get_params()
"""
p = 1; k=2
generate(p,k)

