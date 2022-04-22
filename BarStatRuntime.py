
import os
import os.path
import re
import sys
import collections
from Utils import SPSSutil


INCOMPAT_MSG_KEYWORDS = {'verifyerror', 'security', 'native', 'nullpointer', 'activitynotfound', 'noclass', 'unsatisfiedlink', 
                         'illegalmonitor', 'no_message', 'lang',  'io_exception'}

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

unknown_msg = set()
skip_msg = set()
# taken care of Crash_Immdiately -> no_message, com.badlogic.gdx.utils.j -> 
def get_incompat_msg(msg):
    msg_lower = msg.lower()
    for m in INCOMPAT_MSG_KEYWORDS:
        if m in msg_lower:
            return m 
    if msg in dic.keys():
        unknown_msg.add(msg)
        return dic[msg]
    skip_msg.add(msg)
    return None

 
def collect_fail_msg(info, address):
    year = SPSSutil.get_apkyear(address)
    typ = SPSSutil.get_apktyp(address)
    paragraphs = info.split('\n\n')
    for line in paragraphs[1].splitlines():
        if line.startswith('Failure'):
            lst = line.split()
 
            msg = lst[1][1:-2]
            cnt = int(lst[2])

            cat_msg = get_incompat_msg(msg)
            # if not cat_msg:
            #     print(msg)
            
            

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
    
    print("========== Here is bunch of unknown category exception, but I did group them to certain cateogry see <dic> =========")
    for msg in unknown_msg:
        print(msg)
        
    print("")
    print("========== Here is the msg not considered =============================")
    for msg in skip_msg:
        print(msg)