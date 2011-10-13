#!/opt/local/bin/python
import struct
import time
import binascii, re                     # hex to ascii

u32 = 'u32'
s32 = 's32'
u16 = 'u16'
s16 = 's16'
u8 = 'u8'
s8 = 's8'

""" reading different byte groups """
# TODO automate this. construct the struct strings programatically
def read_u136(byte):
    return str(hex(struct.unpack("=IIIIb", str(byte))[0]))

def read_u32(byte):
    return str(hex(struct.unpack("=I",str(byte))[0]))

def read_s32(byte):
    return str(hex(struct.unpack("=i",str(byte))[0]))

def read_u16(byte):
    return str(hex(struct.unpack("=H",str(byte))[0]))

def read_s16(byte):
    return str(hex(struct.unpack("=h",str(byte))[0]))

def read_u8(byte):
    return str(hex(struct.unpack("=B",str(byte))[0]))

def read_s8(byte):
    return str(hex(struct.unpack("=b",str(byte))[0]))

def read_handler(byte):

    return ret[byte]

def reads (f, type):
    count = int(type[1:]) // 8
    byte = f.read(count)
    """
    In other modules, assuming the module containing the function is 
    called 'module': 
    import module 
    type = ... 
    f = getattr(module, "read_" + type) 
    f(...) 
    """
    read_fn = globals()['read_' + type]
    ubyte = read_fn(byte)
    ubyte = int(ubyte,16)
    hbyte = hex(ubyte)
    sbyte = str(hbyte)
    return sbyte

def write_u32(f, i):
    len = f.write(i)
    return len

"""
.pcap
"""

def pcap_file_header(f):
    print "Magic number: " + reads(f, u32)
    print "Version Major: " + reads(f, u16)
    print "Version Minor: " + reads(f, u16)
    print "Zone: " + reads(f, s32)
    print "Accuracy: " + reads(f, u32)
    print "Slice Size: " + reads(f, u32)
    print "Link Type: " + reads(f, u32)

def pcap_reader(target):
    with open(target, "rb") as f:

        print "      yes really       "
        print "======================="
        # Read the header
        pcap_file_header(f)

        for count in range(1,101):
            # Do stuff with byte.
            sec = reads(f, u32)
            usec = reads(f, u32)
            save_len = reads(f, u32)
            orig_len = reads(f, u32)

            if count > 34 and count < 38 or count > 98:

                isec = int(sec,16)
                iusec = int(usec,16)

                fisec = isec
                fiusec = iusec

                a = 0; b = 0
                while fiusec > 999999 and fiusec < int('0xffffffff',16):
                    fiusec += 1000000
                    fiusec = fiusec % int('0xffffffff',16)
                    fisec -= 1
                    a += 1
                """
                while fiusec < 0:
                    fiusec += 1000000
                    fisec -= 1
                    a += 1
                while fiusec > 999999:
                    fisec = isec + 1;
                    fiusec = iusec - 1000000;
                    b += 1
                """

                ctime = time.strftime('%H:%M:%S', time.gmtime(isec))
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
                
                if a > 0 or b > 0:
                    fctime = time.strftime('%H:%M:%S', time.gmtime(fisec))
                    print "{0:<12} {1:<12} {2:<12} {3:<12}".format('time.sec:', fisec, fctime, '[fixed]')
                    print "{0:<12} {1:<12} {2:<12} {3:<12}".format('time.usec:', fiusec, ' ', '[fixed]')
                    print "{0:>23}  | {1:<5} {2:<5}".format('-sec +sec', a, b)
                

            jmp = int(save_len, 16)
            pkting = f.read(jmp)


"""
.enc
"""
def enc_file_header(f):

    """
    t1 = reads(f, u32)
    t2 = reads(f, u32)
    t3 = reads(f, u32)
    t4 = reads(f, u32)
    t5 = reads(f, u8)
    print "{0:<24} {1:<10} {2:<10} {3:<10} {4:<10} {5:<10}".format('Magic Number:', t1, t2, t3, t4, t5)
    """
    t1 = reads(f, 'u136')
    print "{0:<24} {1:<50}".format('Magic Number:', t1)
    t1 = reads(f, u16)
    print "{0:<24} {1:<10}".format('Record Type:', t1)
    t1 = reads(f, u32)
    print "{0:<24} {1:<10}".format('Record Length:', t1)
    # Version struct
    t1 = reads(f, s16)
    print "{0:<24} {1:<10}".format('Major:', t1)
    t1 = reads(f, s16)
    print "{0:<24} {1:<10}".format('Minor:', t1)
    t1 = reads(f, s16)
    print "{0:<24} {1:<10}".format('DOS Time:', t1)
    t1 = reads(f, s16)
    start = abs(int(t1,16))
    tyear = (start & 0xFE00) >> 9 + 1980 - 1900
    tmon = ((start & 0x1e0) >> 5) - 1
    tday = (start & 0x1f)
    print "{0:<24} {1:<10} Y:{2:<4} M:{3:<2} D:{4:<2}".format('DOS Date:', t1, tyear, tmon, tday)
    t1 = reads(f, s8)
    print "{0:<24} {1:<10}".format('Record Type:', t1)
    network = reads(f, u8)
    print "{0:<24} {1:<10}".format('Network Type:', network)
    t1 = reads(f, s8)
    print "{0:<24} {1:<10}".format('Format Version:', t1)
    t1 = reads(f, u8)
    print "{0:<24} {1:<10}".format('Time Unit:', t1)
    t1 = reads(f, s8)
    print "{0:<24} {1:<10}".format('Compression Field:', t1)
    t1 = reads(f, s8)
    print "{0:<24} {1:<10}".format('Compression Level::', t1)
    t1 = reads(f, s16)
    print "{0:<24} {1:<10}".format('Reserved:', t1)
    # End version struct
         
    return {'network': network,}

enc_network = {
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
def enc_rec_frame2(f, network):
    len = 0

    if network == enc_network['ATM']:
        return -1   # Frame2 record on ATM capture--nope

    # ngsniffer.c:line 1367 
    time_low = reads(f, u16); itime_low = int(time_low, 16)
    len += 16
    time_med = reads(f, u16); itime_med = int(time_med, 16)
    len += 16
    time_high = reads(f, u8); itime_high = int(time_high, 16)
    len += 8
    time_day = reads(f, u8); itime_day = int(time_day, 16)
    len += 8
    size = reads(f, s16); isize = int(size, 16)
    len += 16
    fs = reads(f, u8)
    len += 8
    flags = reads(f, u8)
    len += 8
    true_size = reads(f, s16); itrue_size = int(true_size, 16)
    len += 16
    rsvd = reads(f, s16)
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

def enc_reader(target):
    with open(target, "rb") as f:

        print "      yes really       "
        print "======================="
        # Read the header
        hdr = enc_file_header(f)

        network = int(hdr['network'], 16)

        pkting = True
        for count in range(1,101):

            rec_type = reads(f, u16); irec_type = int(rec_type,16)
            rec_length = reads(f, u32); irec_length = int(rec_length,16)
            irec_length = irec_length & 0x0000FFFF  # only first two bytes are length

            print '\nPacket: {0}'.format(count)
            print '{0:<24} {1:<10} {2:<13}'.format('Record type:', rec_type, irec_type)
            print '{0:<24} {1:<10} {2:<13}'.format('Record length:', rec_length, irec_length)

            # ngsniffer.c:78
            # TODO: better logic here
            frame_len = 0
            if irec_type == 4 or irec_type == 8 or irec_type == 12:
                frame_no = irec_type / 2
                frame_fn = globals()['enc_rec_frame' + str(frame_no)]
                frame_len = frame_fn(f, network)

            jmp = irec_length - frame_len
            print 'jumping {0} bytes'.format(jmp)
            f.read(jmp)

            # This file is major version 4
            # TODO ngsniffer.c:863, emulate it

            if count > 34 and count < 38 or count > 98:
                print 'hi'

def main():
#    pcap_reader("/Users/kenko/Desktop/20110928-170446_timestamp problem.pcap")
    enc_reader("/Users/kenko/Desktop/myencap.enc")

if __name__ == "__main__":
    main()
