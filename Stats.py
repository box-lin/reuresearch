import os
import os.path
import re
import sys
import collections


"""
Usage: python Stats.py <InstallResult/*.txt>

Just to print the summary result to the console.

"""



def get_stat(info, address):
    
    print(address)
    lst = info.splitlines()
    for line in lst:
        if line.startswith("total") or line.startswith("success") or line.startswith("fail"):
            items = line.split()
            print("{}: {}".format(items[0], items[2]))
    print("")

if __name__ == "__main__":

    dir = sys.argv[1]
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            address = os.path.join(parent,fname)
            f = open(address, 'r')
            info = f.read()
            f.close()
            get_stat(info, address)
    

