from pwn import xor
import sys

try:
    filename = sys.argv[1] 
except:
    print("Usage: python3 chall.py <filename>")

f = open(filename, "rb").read()
open(filename+".enc", "wb").write(xor(f, f[:4]))
