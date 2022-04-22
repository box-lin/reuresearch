
import os
import os.path
import re
import sys
import collections

INCOMPAT_MSG ={'DELETE_FAILED_INTERNAL_ERROR', 'INSTALL_FAILED_DUPLICATE_PERMISSION', 'INSTALL_FAILED_INSUFFICIENT_STORAGE', 
               'INSTALL_FAILED_INTERNAL_ERROR', 'INSTALL_FAILED_INVALID_APK', 'INSTALL_FAILED_MISSING_SHARED_LIBRARY',
               'INSTALL_FAILED_NO_MATCHING_ABIS', 'INSTALL_FAILED_OLDER_SDK', 'INSTALL_FAILED_VERSION_DOWNGRADE', 
               'INSTALL_PARSE_FAILED_BAD_MANIFEST', 'INSTALL_PARSE_FAILED_BAD_PACKAGE_NAME', 'INSTALL_PARSE_FAILED_BAD_SHARED_USER_ID',
               'INSTALL_PARSE_FAILED_MANIFEST_MALFORMED', 'INSTALL_PARSE_FAILED_NO_CERTIFICATES', 'INSTALL_PARSE_FAILED_UNEXPECTED_EXCEPTION',
               'NO_MESSAGE'}

FAIL_MSG = set()
YEAR_MSG_COUNT = collections.defaultdict(dict)
YEAR_TOTAL = collections.defaultdict(int)
YEAR_MSG_PERCENT = collections.defaultdict(dict)


def get_year(address):
    name = address.lower()
    bidx = name.find('benign')
    midx = name.find('malware')
    if bidx > 0:
        return name[bidx:bidx+len('benign')+4]
    elif midx > 0:
        return name[midx:midx+len('malware')+4]
    return 'None'

def collect_fail_msg(info, address):
    year = get_year(address)
    paragraphs = info.split('\n\n')
    for line in paragraphs[1].splitlines():
        if line.startswith('Failure'):
            lst = line.split()
            
            msg = lst[1][1:-2]
            cnt = int(lst[2])
            
            if msg in INCOMPAT_MSG:
                # increase the cnt
                try:
                    YEAR_MSG_COUNT[year][msg] += cnt
                # not exit key yet, assign cnt
                except:
                    YEAR_MSG_COUNT[year][msg] = cnt
                    
                YEAR_TOTAL[year] += cnt
                FAIL_MSG.add(msg)
        
def compute_percentage():
    for year, dict in YEAR_MSG_COUNT.items():
        total = YEAR_TOTAL[year]
        for msg, cnt in dict.items():
            YEAR_MSG_PERCENT[year][msg] = float(cnt/total)

def print_console():
    for year, dict in YEAR_MSG_PERCENT.items():
        print(year + ': -----------------------')
        total = 0
        for msg, percent in dict.items():
            total += percent
            print(msg + ': ' + str(percent))
        print(total)
        print('')
            
    
if __name__ == '__main__':
    dir = sys.argv[1]
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            address = os.path.join(parent,fname)
            f = open(address, 'r')
            info = f.read()
            f.close()
            collect_fail_msg(info,address)
            
    compute_percentage()
    print_console()
 