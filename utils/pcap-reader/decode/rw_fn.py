#!/opt/local/bin/python
import struct
import time
import binascii, re                     # hex to ascii

# Sourcing local python files
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import rw_fn

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
