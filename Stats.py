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
    totalcnt, successcnt, failcnt = 0, 0, 0
    for line in lst:
        if line.startswith("total") or line.startswith("success") or line.startswith("fail"):
            items = line.split()
            print("{}: {}".format(items[0], items[2]))
            if line.startswith("total"):
                totalcnt = int(items[2])
            elif line.startswith("success"):
                successcnt = int(items[2])
            elif line.startswith("fail"):
                failcnt = int(items[2])
    print('Success rate: ', float(successcnt/totalcnt))
    print('Fail rate: ', float(failcnt/totalcnt))
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
    

