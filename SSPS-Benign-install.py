import os
import os.path
import re
import sys
import csv 
from Utils import SPSSutil
from openpyxl import Workbook, workbook, load_workbook

def collect_ins_success(data, fname_lower):
    listlines = data.splitlines()
    if len(listlines) <= 1: return 
    
    apkyear = SPSSutil.get_apkyear(fname_lower)
    apilevel = SPSSutil.get_apkapi(fname_lower)
    typ = SPSSutil.get_apktyp(fname_lower)
    apiyear = SPSSutil.get_apiyear(apilevel)
    
    for apknamestr in listlines[1:]:
        apkname = apknamestr.strip()
        apkinstall[(apkname, apkyear, typ)] = [True, apilevel, apiyear]
        
def collect_ins_fail(data, fname_lower):
    listlines = data.splitlines()
    if len(listlines) <= 1: return  
    
    apkyear = SPSSutil.get_apkyear(fname_lower)
    apilevel = SPSSutil.get_apkapi(fname_lower)
    typ = SPSSutil.get_apktyp(fname_lower)
    apiyear = SPSSutil.get_apiyear(apilevel)
    
    for row in listlines[1:]:
        if row.startswith('Failure'):
            continue
        else:
            apkname = row.strip()
            apkinstall[(apkname, apkyear, typ)] = [False, apilevel, apiyear]

if __name__ == "__main__":
    # (apk, typ, year):boolean
    apkinstall = {}
    apksdk = {}
    log_path = "InstallResult"
    sdk_path = "DataParse/benign-minsdk"
    
    # prepare the apksdk dictionary
    for parent,dirnames, filenames in os.walk(sdk_path):
        for fname in filenames:
            fname_lower = fname.lower() 
            address = os.path.join(parent,fname)  
            # read the txt
            f = open(address, 'r')
            info = f.read()
            f.close()
            for line in info.splitlines():
                lst = line.split()
                
                typ = lst[0]
                apkyear = lst[1]
                apkname = lst[2]
                sdk = lst[3]
                
                apksdk[(apkname, apkyear, typ)] = sdk
    
    # prepare the apkinstall dictionary
    for parent,dirnames, filenames in os.walk(log_path):
        for fname in filenames:
            fname_lower = fname.lower()
            if fname_lower.find('benign') < 0: continue
            print('scanning: ', fname_lower)
            address = os.path.join(parent,fname)  
            # read the txt
            f = open(address, 'r')
            info = f.read()
            f.close()
            
            paragraphs = info.split('\n\n')
            success_para = paragraphs[2]
            fail_para = paragraphs[3]
            
            collect_ins_success(success_para, fname_lower)
            collect_ins_fail(fail_para, fname_lower)
    
    cnt = 0 
    # append minsdk to apkinstall dictionary
    for lst1 in apkinstall.keys():
        if lst1 in apksdk.keys():
            minsdk = apksdk[lst1]
        else:
            minsdk = str(0)
            cnt += 1
        apkinstall[lst1].append(minsdk)
    print("Total apks: ", len(apkinstall.keys()))
    print("Number of apk didnt compute minsdk (default them to 0 minsdk): ", cnt)

    # (tupkey):[#success, #fail]
    ans = SPSSutil.get_dic()
    for lst1, lst2 in apkinstall.items():
        apkname, apkyear, typ = lst1 
        isCompat, apilevel, apiyear, minsdk = lst2    
        tupkey = (minsdk, apilevel, apkyear, apiyear)
        if isCompat:
            ans[tupkey][0] += 1
        else:
            ans[tupkey][1] += 1

            
            
    # --------------------------------------------------------------------- IO ------------------------------------------------------------------ #
    # NOTE uncomment this to print console
    # console print
    # for lst, stat in ans.items():
    #     num_succ, num_fail = stat 
    #     total = num_succ + num_fail
    #     if total != 0:
    #         rate = float(num_fail/total)
    #     else: 
    #         rate = 0.0
    #     print(lst, '\tFailure Rate: ', rate)
    
    
    # # write to excel 
    wb = Workbook()
    ws = wb.active
    ws.title = 'SSPS'
    ws.append(['failure rate', 'min sdk', 'api year', 'year', 'api\'s year ', 'api-year', 'api-min'])
    for lst, stat in ans.items():
        num_succ, num_fail = stat 
        total = num_succ + num_fail
        if total != 0:
            rate = float(num_fail/total)
        else: 
            rate = 0.0
        minsdk, apilevel, apkyear, apiyear = lst[0], lst[1], lst[2], lst[3]
        cal1, cal2 = str(int(apiyear) - int(apkyear)), str(int(apilevel) - int(minsdk))
        ws.append([rate, minsdk, apilevel, apkyear, apiyear, cal1, cal2])
    wb.save('Data/InstallSPSS-2018-2019.xlsx')
    print("Result write into Data/InstallSPSS-2018-2019.xlsx completed!")
    
        