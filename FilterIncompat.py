import os
import os.path
import re
import sys
import collections


"""
Usage: python FilterIncompat <InstallResult/*.txt>
"""

INSTALL_COMPAT_MSG = {
    "Could not access the Package Manager", "DELETE_FAILED_INTERNAL_ERROR", "INSTALL_FAILED_CONFLICTING_PROVIDER", 
    "INSTALL_FAILED_DUPLICATE_PERMISSION", "INSTALL_FAILED_SHARED_USER_INCOMPATIBLE", "INSTALL_FAILED_UID_CHANGED",
    "INSTALL_FAILED_UPDATE_INCOMPATIBLE", "INSTALL_PARSE_FAILED_CERTIFICATE_ENCODING", "must either specify a package size or an APK file", 
    "INSTALL_PARSE_FAILED_MANIFEST_MALFORMED"
}

RUNTIME_COMPAT_MSG = {}


def retrive_detail(incompat_dict, details):
    pass

def filter_stats(stats):
    res = {}
    for item in stats:
        lst = item.split()
        name = lst[1]
        cnt = lst[2]
        if name not in INSTALL_COMPAT_MSG:
            res[name] = cnt 
    print(res)
    return res 


def filter_incompat(info):
    
    lst = info.splitlines()
    
    stats = []
    scan = False
    for line in lst:
        if scan and line.strip() == "":
            break 
        if scan:
            stats.append(line)
        if line.startswith("<-------------- Fail effect ----------------->"):
            scan = True
    incompat_dict = filter_stats(stats)
    
    details = collections.defaultdict(set)
    scan = False 




if __name__ == "__main__":

    dir = sys.argv[1]
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            address = os.path.join(parent,fname)
            f = open(address, 'r')
            info = f.read()
            f.close()
            filter_incompat(info)
    

