import os
import os.path
import re
import sys
import collections

"""
Cases of Success:
    1. logcat content with '--------- beginning of /dev/log/main' and monkey no content
    2. logcat and monkey all did not found crash keyword

Cases of Fail:
    1. logcat size is 0
    2. locat size > 0 and found crash in monkey
    
"""
if __name__ == "__main__":
    rootdir = sys.argv[1]

    for parent, dirnames, filenames in os.walk(rootdir):
         # key failure per distinct of apks
        fail_apks = collections.defaultdict(set)

        # buffer for success running apks
        # key apk value 1 means only check its logcat or monkey, 2 means both logcat and monkey checked and no crash founded.
        buffer = {}

        # add apk to success when buffer[apk] = 2
        success = set()

        visited = set()

        fulladdress =""
        
        # can't launch.
        crash_immdiate = set()
        for filename in filenames:
            # cut from .logcat or .monkey postfix
            apkname = filename[0:-7]
            fullname=os.path.join(parent,filename)

            # for use of write out file name
            fulladdress = fullname

            # if apk has been founded previously crash immiately, check next trace
            if apkname in crash_immdiate: 
                visited.add(fullname)
                continue

            # read the trace
            f = open(fullname, 'r', errors="ignore")
            info = f.read()
            f.close()

            # crashed immediately, go to next one
            if len(info) <= 2: 
                fail_apks['Immdiately Crash'].add(apkname)
                crash_immdiate.add(apkname)
                visited.add(fullname)
                continue
            
            # Handles the successful running apks, locat and monkey not found crash consider success
            # ftype = filename[-7:]
            not_crash = info.find('CRASH') < 0 or info.find('Short') < 0  or info.find('Long') < 0
            if not_crash and fullname not in visited:
                if apkname not in buffer:
                    buffer[apkname] = 1   
                else:
                    buffer[apkname] += 1
                visited.add(fullname)
                if buffer[apkname] >=2: success.add(apkname)
                continue

            # Otherwise must some crash keyword founded.
            info_lst = info.splitlines()
            fail_info = []
            for i, line in enumerate(info_lst):
                if line.find('CRASH') > 0:
                    try:
                        short_msg = info_lst[i+1]
                        try:
                            failure_name = short_msg.split()[3] 
                            fail_apks[failure_name].add(apkname)
                        except:
                            continue   
                    except:
                        continue

        # print result
        cut = 0
        for i in range(len(fulladdress)-1,-1,-1):
            if fulladdress[i] == '/':
                cut = i
                break
        write_name_temp = fulladdress[0:cut]
        write_file_name = ""
        for c in write_name_temp:
            if c != '/':
                write_file_name += c


        os.system("mkdir -p RuntimeResult")
        output = open('./RuntimeResult/' + write_file_name +'-res.txt', 'w')

        print("===================== Runtime Results for <{}> =====================".format(str(write_file_name)))
        output.write("===================== Runtime Results for <{}> =====================\n".format(str(write_file_name)))

        success_cnt = len(success)
        fail_cnt = 0
        for k, v in fail_apks.items():
            fail_cnt += len(v)
        total_cnt = success_cnt+fail_cnt

        print("total Apks: " +str(total_cnt))
        print("success apks: "+str(success_cnt))
        print("fail apks: "+str(fail_cnt))

        output.write("total Apks: {}\n".format(total_cnt))
        output.write("success apks: {}\n".format(success_cnt))
        output.write("fail apks: {}\n".format(fail_cnt))

        print("")
        output.write('\n')

        for k, v in fail_apks.items():
            print("Failure: [{}]: {}".format(k, len(v)))
            output.write("Failure: [{}]: {}\n".format(k, len(v)))

        output.write('\n')
        output.write('------------------------- details -----------------------------\n')
        

        for k, v in fail_apks.items():
             output.write("Failure: [{}]: {}\n".format(k, len(v)))
             for apk in v:
                 output.write("         " + str(apk) + "\n")


        output.close()
