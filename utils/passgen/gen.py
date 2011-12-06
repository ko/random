#!/usr/local/bin/python2.7
import argparse
import getpass
import os

def read_key():
    keypath = os.getenv('HOME') + '/.ssh/id_rsa.pub'
    with open(keypath,'rb') as f:
        for line in f:
            print line

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

def generate(params):
    s = params['hostname'] 
    u = params['user']
    p = params['pass']
    print '{0},{1},{2}'.format(s,u,p)



read_key()
p = get_params()
generate(p)

