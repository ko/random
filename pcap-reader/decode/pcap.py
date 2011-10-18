#!/opt/local/bin/python
import struct
import time
import binascii, re                     # hex to ascii

# Sourcing local python files
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import rw_fn as rw

"""
.pcap
"""

def magic_number():
    return int('0xa1b2c3d4', 16)

def file_header(f):
    print "Magic number: " + rw.reads(f, rw.u32)
    print "Version Major: " + rw.reads(f, rw.u16)
    print "Version Minor: " + rw.reads(f, rw.u16)
    print "Zone: " + rw.reads(f, rw.s32)
    print "Accuracy: " + rw.reads(f, rw.u32)
    print "Slice Size: " + rw.reads(f, rw.u32)
    print "Link Type: " + rw.reads(f, rw.u32)

def reader(target, badpkt):
    with open(target, "rb") as f:

        print "      yes really       "
        print "======================="
        # Read the header
        file_header(f)

        count = 1;
        while 1:
            # Do stuff with byte.
            sec = rw.reads(f, rw.u32)
            usec = rw.reads(f, rw.u32)
            save_len = rw.reads(f, rw.u32)
            orig_len = rw.reads(f, rw.u32)

            if count == (badpkt+2):
                break;

            if count > (badpkt-3) and count < (badpkt+3):

                isec = int(sec,16)
                iusec = int(usec,16)

                fisec = isec
                fiusec = iusec

                a = 0
                while fiusec > 999999 and fiusec < int('0xffffffff',16):
                    fiusec += 1000000
                    fiusec = fiusec % int('0xffffffff',16)
                    fisec -= 1
                    a += 1

                ctime = time.strftime('%Y %m %d - %H:%M:%S', time.gmtime(isec))
                scount = str(count)
                sec_dec = str(isec)
                usec_dec = str(iusec)
                usec_twos = str(hex(((abs(iusec) ^ 0xffffffff) + 1) & 0xffffffff))
                usec_twos_dec = str(int(usec_twos,16))
                iusec_twos_dec = int(usec_twos_dec)

                print "\n"
                print "{0:<12} {1:<12}".format('Packet:',scount)
                print "{0:<12} {1:<12}| {2:<12}| {3:<12}".format('time.sec:', sec,sec_dec,ctime)
                print "{0:<12} {1:<12}| {2:<12}".format('time.usec:', usec,usec_dec)
                print "{0:>23}  | {1:<12} [2\'s]".format(usec_twos,usec_twos_dec)
                
                if a > 0:
                    fctime = time.strftime('%H:%M:%S', time.gmtime(fisec))
                    print "{0:<12} {1:<12} {2:<12} {3:<12}".format('time.sec:', fisec, fctime, '[fixed]')
                    print "{0:<12} {1:<12} {2:<12} {3:<12}".format('time.usec:', fiusec, ' ', '[fixed]')
                    print "{0:>23}  | {1:<5}".format('-sec', a)
               
            count += 1
            jmp = int(save_len, 16)
            pkting = f.read(jmp)

