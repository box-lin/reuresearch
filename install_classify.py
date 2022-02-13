import os
import subprocess
import sys
import re
import collections



apk_installed = set()
apk_failed = collections.defaultdict(set)




def print_result(out, logname):

    print("===================== Installation Results for <{}> =====================".format(str(logname)))
    out.write("===================== Installation Results for <{}> =====================\n".format(str(logname)))

    
    success_cnt = len(apk_installed)
    fail_cnt = 0
    for k, v in apk_failed.items():
        fail_cnt += len(v)

    total_apk = success_cnt + fail_cnt
    print("total apks: " + str(total_apk))
    out.write("total apks: " + str(total_apk) +'\n')

    print("success apks: " + str(success_cnt))
    out.write("success apks: " + str(success_cnt) +'\n')

    print("fail apks: " + str(fail_cnt))
    out.write("fail apks: " + str(fail_cnt) +'\n')

    print("")
    out.write('\n')

    print('<-------------- Fail effect ----------------->')
    out.write('<-------------- Fail effect ----------------->' +'\n')

    for k, v in apk_failed.items():
        print('Failure ' + str(k) + ": " + str(len(v)))
        out.write('Failure ' + str(k) + ": " + str(len(v)) +'\n')

  
    # write very detail apks in each failure 
    out.write('\n')
    out.write('------------------------- details -----------------------------\n')
    for k, v in apk_failed.items():
        out.write('Failure ' + str(k) + ": " + str(len(v)) +'\n')
        for apk in v:
            out.write("       " + str(apk) + '\n')
    

def classify_each(install_item):
    lst = install_item.splitlines()
    try:
        apk_num = lst[0].split()[4]
    except:
        return
    
    install_OK = install_item.find('installed successfully') >= 0 and install_item.find('unnstalled successfully') >= 0
    if install_OK:
        apk_installed.add(apk_num)
        return 
    
    for l in lst:
        if l.startswith('Failure'):
	    try:
            	fail_reason = l.split()[1]
	    except:
                continue
            apk_failed[fail_reason].add(apk_num)




if __name__ == "__main__":

    log_name = sys.argv[1]
    with open(log_name,'r') as f:
        line = f.readline()
 
        item, flag = "", False
        while line:
            if line.startswith("====================================== Install INDIVIDUAL APP:"):
                flag = True
            elif flag and line.strip() == "":
                classify_each(item)
                flag = False
                item = ""
            
            if flag: item+=line
            line = f.readline()

        # last item not yet classify!
        classify_each(item)
    f.close()

    os.system("mkdir -p InstallResult")
   
    filename = log_name
    if '/' in log_name:
        filename = ""
        for i in range(len(log_name)-1, -1,-1):
            if log_name[i] == '/':break
            filename = log_name[i] + filename
            

    output = open('./InstallResult/' + filename +'-res.txt', 'w')
    # print and save result
    print_result(output, filename)
    output.close()
