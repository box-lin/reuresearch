from distutils.log import error
import os
import os.path
import re
import sys
import collections

 

def is_no_fail(text):
    return text.find('Crash') < 0 and text.find('Fail') < 0 and text.find('crash') < 0 and  text.find('fail') < 0 and text.find('CRASH') < 0 

def is_fail(text):
    return not is_no_fail(text)   

if __name__ == "__main__":
    rootdir = sys.argv[1]
    
    # traver through dir
    for parent, dirnames, filenames in os.walk(rootdir):
        
        fail_apks = collections.defaultdict(set)
        success = set()
        
        for filename in filenames:
            
            # if current file is logcat, we do the analysis and find
            # the corresponding monkey file, otherwise continue.
            logcat_idx = filename.find('.logcat')
            if logcat_idx < 0: continue 
            
            
            apkname = filename[0:-7]
            
            # read logcat
            logcat_address = os.path.join(parent,filename)
            f = open(logcat_address, 'r', errors='ignore')
            logcat_info = f.read()
            f.close()
            
            # read monkey
            monkey_address = logcat_address[:-7] + '.monkey'
            f = open(monkey_address, 'r', errors='ignore')
            monkey_info = f.read()
            f.close()
            
            # case 1: if length of logcat and length of monkey is zero [Crash Immdiately]
            if len(logcat_info) == 0 and len(monkey_info) == 0:
                fail_apks['Crash Immdiately'].add(apkname)
                continue
            
            # case 2: monkey info empty and locat no fail keyword it is sucess
            if len(logcat_info) > 0 and len(monkey_info) == 0 and is_no_fail(logcat_info):
                success.add(apkname)
                continue 
            
            # general case when no error keyword found 
            if is_no_fail(logcat_info) and is_no_fail(monkey_info):
                success.add(apkname)
                continue 
            
            # general case when error keyword found
            if is_fail(logcat_info) or is_fail(monkey_info):
                monkey_info_lst = monkey_info.splitlines()
                for i, line in enumerate(monkey_info_lst):
                    if line.find('CRASH') > 0:
                        try:
                            short_msg = monkey_info_lst[i+1]
                            try:
                                failure_name = short_msg.split()[3] 
                                fail_apks[failure_name].add(apkname)
                            except:
                                continue   
                        except:
                            continue
              
        # after each iteration is completed, save the result
        cur_address = os.path.join(parent)
        cur_address.replace('/','')
        os.system("mkdir -p RuntimeResult")
        output = open('./RuntimeResult/' + cur_address +'-res.txt', 'w')

        print("===================== Runtime Results for <{}> =====================".format(str(cur_address)))
        output.write("===================== Runtime Results for <{}> =====================\n".format(str(cur_address)))

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
        