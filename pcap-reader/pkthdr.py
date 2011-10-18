#!/opt/local/bin/python
import struct
import time
import binascii, re                     # hex to ascii

# Sourcing local python files
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
cmd_folder = cmd_folder
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from decode import enc, pcap
from decode import rw_fn as rw

magic_number = {
    pcap.magic_number: 'pcap',
    enc.magic_number: 'enc',
}
def match_magic_number(target):
    with open(target, 'rb') as f:
        magic = rw.reads(f, rw.u32)
        imagic = int(magic, 16)  
        
        a = magic_number.get(imagic, 'default')    
        print a
    return 

def main():

    type = sys.argv[1]
    target = sys.argv[2]
    badpkt = int(sys.argv[3])

    if type == 'enc':
        enc.reader(target, badpkt)
    elif type == 'pcap':
        pcap.reader(target, badpkt)

if __name__ == "__main__":
    main()
