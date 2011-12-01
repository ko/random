
# to include modules in local directory
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from pymsasid import pymsasid as pyms

sauce = 'D:\ko\Dropbox\git\toolkit\x86-call-list\KeyMe2.exe'
prog = pyms.Pymsasid(hook = pyms.PEFileHook, source = sauce)
inst = prog.disassemble(prog.pc)
print inst
