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
.enc
"""
def magic_number():
    return int('0x4e535254', 16)

def file_header(f):

    """
    t1 = rw.reads(f, rw.u32)
    t2 = rw.reads(f, rw.u32)
    t3 = rw.reads(f, rw.u32)
    t4 = rw.reads(f, rw.u32)
    t5 = rw.reads(f, rw.u8)
    print "{0:<24} {1:<10} {2:<10} {3:<10} {4:<10} {5:<10}".format('Magic Number:', t1, t2, t3, t4, t5)
    """
    t1 = rw.reads(f, 'u136')
    print "{0:<24} {1:<50}".format('Magic Number:', t1)
    t1 = rw.reads(f, rw.u16)
    print "{0:<24} {1:<10}".format('Record Type:', t1)
    t1 = rw.reads(f, rw.u32)
    print "{0:<24} {1:<10}".format('Record Length:', t1)
    # Version struct
    t1 = rw.reads(f, rw.s16)
    print "{0:<24} {1:<10}".format('Major:', t1)
    t1 = rw.reads(f, rw.s16)
    print "{0:<24} {1:<10}".format('Minor:', t1)
    t1 = rw.reads(f, rw.s16)
    print "{0:<24} {1:<10}".format('DOS Time:', t1)
    t1 = rw.reads(f, rw.s16)
    start = abs(int(t1,16))
    tyear = (start & 0xFE00) >> 9 + 1980 - 1900
    tmon = ((start & 0x1e0) >> 5) - 1
    tday = (start & 0x1f)
    print "{0:<24} {1:<10} Y:{2:<4} M:{3:<2} D:{4:<2}".format('DOS Date:', t1, tyear, tmon, tday)
    t1 = rw.reads(f, rw.s8)
    print "{0:<24} {1:<10}".format('Record Type:', t1)
    network = rw.reads(f, rw.u8)
    print "{0:<24} {1:<10}".format('Network Type:', network)
    t1 = rw.reads(f, rw.s8)
    print "{0:<24} {1:<10}".format('Format Version:', t1)
    t1 = rw.reads(f, rw.u8)
    print "{0:<24} {1:<10}".format('Time Unit:', t1)
    t1 = rw.reads(f, rw.s8)
    print "{0:<24} {1:<10}".format('Compression Field:', t1)
    t1 = rw.reads(f, rw.s8)
    print "{0:<24} {1:<10}".format('Compression Level::', t1)
    t1 = rw.reads(f, rw.s16)
    print "{0:<24} {1:<10}".format('Reserved:', t1)
    # End version struct
         
    return {'network': network,}

network = {
        'TRING':    0,
        'ENET':     1,
        'ARCNET':   2,
        'STARLAN':  3,
        'PCNW':     4,
        'LOCALTALK':5,
        'SYNCHRO':  7,
        'ASYNC':    8,
        'FDDI':     9,
        'ATM':      10,
        }
def rec_frame2(f, network):
    len = 0

    if network == network['ATM']:
        return -1   # Frame2 record on ATM capture--nope

    # ngsniffer.c:line 1367 
    time_low = rw.reads(f, rw.u16); itime_low = int(time_low, 16)
    len += 16
    time_med = rw.reads(f, rw.u16); itime_med = int(time_med, 16)
    len += 16
    time_high = rw.reads(f, rw.u8); itime_high = int(time_high, 16)
    len += 8
    time_day = rw.reads(f, rw.u8); itime_day = int(time_day, 16)
    len += 8
    size = rw.reads(f, rw.s16); isize = int(size, 16)
    len += 16
    fs = rw.reads(f, rw.u8)
    len += 8
    flags = rw.reads(f, rw.u8)
    len += 8
    true_size = rw.reads(f, rw.s16); itrue_size = int(true_size, 16)
    len += 16
    rsvd = rw.reads(f, rw.s16)
    len += 16

    print "Frame 2 ({0:<5} bytes)".format(len)
    print "---------------------"
    print "{0:<4}{1:<20} {2:<10} {3:<10}".format(' ', 'Time low:', time_low, itime_low)
    print "{0:<4}{1:<20} {2:<10} {3:<10}".format(' ', 'Time med:', time_med, itime_med)
    print "{0:<4}{1:<20} {2:<10} {3:<10}".format(' ', 'Time high:', time_high, itime_high)
    print "{0:<4}{1:<20} {2:<10} {3:<10}".format(' ', 'Time day:', time_low, itime_low)
    print "{0:<4}{1:<20} {2:<10} {3:<10}".format(' ', 'Size:', size, isize)
    print "{0:<4}{1:<20} {2:<10} {3:<10}".format(' ', 'True Size:', true_size, itrue_size)

    return len 

def reader(target):
    with open(target, "rb") as f:

        print "      yes really       "
        print "======================="
        # Read the header
        hdr = file_header(f)

        network = int(hdr['network'], 16)

        pkting = True
        for count in range(1,101):

            rec_type = rw.reads(f, rw.u16); irec_type = int(rec_type,16)
            rec_length = rw.reads(f, rw.u32); irec_length = int(rec_length,16)
            irec_length = irec_length & 0x0000FFFF  # only first two bytes are length

            print '\nPacket: {0}'.format(count)
            print '{0:<24} {1:<10} {2:<13}'.format('Record type:', rec_type, irec_type)
            print '{0:<24} {1:<10} {2:<13}'.format('Record length:', rec_length, irec_length)

            # ngsniffer.c:78
            # TODO: better logic here
            frame_len = 0
            if irec_type == 4 or irec_type == 8 or irec_type == 12:
                frame_no = irec_type / 2
                frame_fn = globals()['rec_frame' + str(frame_no)]
                frame_len = frame_fn(f, network)

            jmp = irec_length - frame_len
            print 'jumping {0} bytes'.format(jmp)
            f.read(jmp)

            # This file is major version 4
            # TODO ngsniffer.c:863, emulate it

            if count > 34 and count < 38 or count > 98:
                print 'hi'
