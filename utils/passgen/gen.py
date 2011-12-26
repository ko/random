#!/usr/local/bin/python2.7
import argparse
import getpass
import os
import random
import hashlib

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

    h = params['hostname'] 
    u = params['user']
    p = params['pass']

    # salt pvt key with service hostname + username
    k['lines'].append(h)
    k['lines'].append(u)
    salted = ''
    for line in k['lines']:
        salted += line

    # hash the salted pvt key
    #   keyspace for the future seed() is hella small now
    manager = hashlib.sha1()
    manager.update(salted)
    hashed = manager.hexdigest()

    # and now the passphrase
    index = 0
    passphrase = params['pass']
    hlen = hashed.__len__()
    plen = passphrase.__len__()
    if hlen > plen:
        passphrase = (passphrase*((hlen/plen+1)))[:plen]
        print passphrase
    elif hlen < plen:           
        hashed = (hashed*((plen/hlen+1)))[:hlen]
        print hashed

    hashed = [ord(a) ^ ord(b) for a,b in zip(hashed,passphrase)]

    # probably not remembering this piece off the top of my head
    for i in range(0,passlength):
        index = i % hashed.__len__()
        random.seed(hashed[index])
        random.jumpahead((i+1)*(i+2))
        val = random.randint(ascii_min, ascii_max) 
        s += chr(val)

    print '--->[' + s + ']<---'

k = read_key()
p = 1
p = get_params()
generate(p,k,16)

