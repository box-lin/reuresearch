
import os
import os.path
import re
import sys
import collections
from Utils import SPSSutil
import collections




yearTotal = collections.defaultdict(int)

def get_stat(info, address):
    address_lower = address.lower()
    year = SPSSutil.get_apkyear(address_lower)
    typ = SPSSutil.get_apktyp(address_lower)
    tupkey = (typ, year)
    totalcnt = int(info.splitlines()[1].split()[2])
    yearTotal[tupkey] += totalcnt
    

if __name__ == "__main__":

    dir = sys.argv[1]
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            address = os.path.join(parent,fname)
            f = open(address, 'r')
            info = f.read()
            f.close()
            get_stat(info, address)
    
    for tupkey, total in yearTotal.items():
        print(tupkey, 'total apks: ', total)
    

