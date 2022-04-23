
import os
import os.path
import re
import sys
import collections
from Utils import SPSSutil

YEAR_MSG_COUNT = collections.defaultdict(dict)
YEAR_TOTAL = collections.defaultdict(int)
YEAR_MSG_PERCENT = collections.defaultdict(dict)


# Highest level
dic = {'java.io.FileNotFoundException':'io_exception', 
       'java.io.IOException': 'io_exception',
       'android.view.InflateException':  'io_exception',
       'android.util.SuperNotCalledException': 'native', 
       'Crash_Immdiately': 'no_message',
       'android.database.sqlite.SQLiteException': 'io_exception',
       'android.database.sqlite.SQLiteCantOpenDatabaseException': 'io_exception',
       'android.content.res.Resources$NotFoundException':'activitynotfound',
       'android.system.ErrnoException':'io_exception',
       'android.database.CursorIndexOutOfBoundsException': 'io_exception',
       'libcore.io.ErrnoException':'io_exception',
       'com.mobclix.android.sdk.Mobclix$MobclixPermissionException':'verifyerror',
       'android.util.AndroidRuntimeException' :'activitynotfound',
       'android.database.sqlite.SQLiteReadOnlyDatabaseException': 'io_exception', 
       }

# Intermediate level
INCOMPAT_MSG_KEYWORDS = {'verifyerror', 'security', 'native', 'nullpointer', 'activitynotfound', 'noclass', 'unsatisfiedlink', 
                         'illegalmonitor', 'no_message',  'io_exception'}
# Lowest
LANG = 'lang'

 

unknown_msg = collections.defaultdict(int)
skip_msg = collections.defaultdict(int)
fail_msg = set()
def get_incompat_msg(msg):
    
    # the return is is lowercase identical to keyword dic
    if msg in dic.keys():
        unknown_msg[msg] += 1
        return dic[msg]
    
    # then check for keywords
    msg_lower = msg.lower()
    for m in INCOMPAT_MSG_KEYWORDS:
        if m in msg_lower:
            return m 
        
    # lang is so common, so check at last stage
    if LANG in msg_lower:
        return LANG 
    # here is msg skipped.
    skip_msg[msg] += 1
    return None
    

 
def collect_fail_msg(info, fname_lower):
    year = SPSSutil.get_apkyear(fname_lower)
    typ = SPSSutil.get_apktyp(fname_lower)
    keystr = typ+year
    paragraphs = info.split('\n\n')
    for line in paragraphs[1].splitlines():
        if line.startswith('Failure'):
            lst = line.split()
            msg = lst[1][1:-2]
            cnt = int(lst[2])
            cat_msg = get_incompat_msg(msg)
            if cat_msg:
                try:
                    YEAR_MSG_COUNT[keystr][cat_msg] += cnt
                except:
                    YEAR_MSG_COUNT[keystr][cat_msg] = cnt
                YEAR_TOTAL[keystr] += cnt     

def compute_percentage():
    for keystr, dict in YEAR_MSG_COUNT.items():
        total = YEAR_TOTAL[keystr]
        for msg, cnt in dict.items():
            YEAR_MSG_PERCENT[keystr][msg] = float(cnt/total)

def print_console():
    for keystr, dict in YEAR_MSG_PERCENT.items():
        print(keystr + ': -----------------------')
        total = 0
        for msg, percent in dict.items():
            total += percent
            print(msg + ': ' + str(percent))
        print(total)
        print('')


def notice1():
    print("========== Here are bunch of unknown category exception, but I did group them to certain cateogry see <dic> =========")
    for msg, freq in unknown_msg.items():
        print(msg, freq)

def notice2():
    print("")
    print("========== Here are the msg not being considered =============================")
    for msg, freq in skip_msg.items():
        print(msg, freq)
        
if __name__ == '__main__':
    dir = sys.argv[1]
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            fname_lower = fname.lower() 
            address = os.path.join(parent,fname)
            f = open(address, 'r')
            info = f.read()
            f.close()
            collect_fail_msg(info, fname_lower)
            
    # unknown category hardcoded notice        
    # notice1()
    
    # msg skipped notice
    # notice2()
    
    compute_percentage()
    print_console()
