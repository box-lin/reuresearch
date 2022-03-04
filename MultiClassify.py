# an example of multi-apk in the file malware2019.csv:
# "com.elfinapp.jxtxdq". 
# "00022D057443AC60334E3DD676F30A3B4C2837DE54C09A4CB85A28D950C4E2A9".
# "03492E5AE39B8CA96D9530E1418C2A22269D8A3BF9DCC175783EA937B971367D".
# "A091D374B08EBF6D2F6D115C19832E3DD80852C566E537E78CCEF4BE557ECEF3".
# they are the same app (application "com.elfinapp.jxtxdq") but different APKs.

# If these three APKs successfully covered all Android APIs (19,21-27), there is no incompatibility even though some APKs failed in some APIs.
# For example, if 00022D057443AC60334E3DD676F30A3B4C2837DE54C09A4CB85A28D950C4E2A9.apk succeeded in APIs 19/21/22 (and failed in other APIs) , 
#       03492E5AE39B8CA96D9530E1418C2A22269D8A3BF9DCC175783EA937B971367D succeeded in APIs 23/24/25 (and failed in other APIs), 
#       and A091D374B08EBF6D2F6D115C19832E3DD80852C566E537E78CCEF4BE557ECEF3 succeeded in APIs 26/27 (and failed in other APIs)
# we think that the app "com.elfinapp.jxtxdq" does not have any incompatibility.

# Otherwise, if three APKs 00022D057443AC60334E3DD676F30A3B4C2837DE54C09A4CB85A28D950C4E2A9.apk, 
#           03492E5AE39B8CA96D9530E1418C2A22269D8A3BF9DCC175783EA937B971367D, 
#           and A091D374B08EBF6D2F6D115C19832E3DD80852C566E537E78CCEF4BE557ECEF3 failed in one API such as API 27,
# we say that app "com.elfinapp.jxtxdq" has an incompatibility.  
# The rest may be inferred by analogy.

import collections
import csv 
import os
import subprocess
import sys 

# {apk:name} FROM csv Record
ApksToName = collections.defaultdict()

# {API:{apk1, apk2, ....}}  FROM classified result
APIToSuccessApk = collections.defaultdict(set)
APIToFailureApk = collections.defaultdict(set)
 
# {apkname:[....]len7  Intermediate Buffer for Sucess
NameToSlot = collections.defaultdict(list)

# result
TotalNames = set()
SucessCompat = set()
FailCompat = set()
UncoverSet = set()

def print_result():
    print("============= Multi Classification <{}> See if API19, 21-27 covered with compat =============".format(result_dir))
    print("Total app name: {}".format(len(TotalNames)))
    print("Success app name: {}".format(len(SucessCompat)))
    print("Fail app name: {}".format(len(FailCompat)))
    print("Uncover app name: {}".format(len(UncoverSet)))
    
    
    ## ----- Write to file ------
    os.system("mkdir -p MultiCompatResult")
    filename = result_dir
    if '/' in result_dir:
        filename = ""
        for i in range(len(result_dir)-1, -1,-1):
            if result_dir[i] == '/':break
            filename = result_dir[i] + filename
        
    output = open('./MultiCompatResult/Multi-' + filename +'-res.txt', 'w')
    output.write("============= Multi Classification <{}> See if API19, 21-27 covered with compat =============\n".format(result_dir))
    output.write("Total app name: {}\n".format(len(TotalNames)))
    output.write("Success app name: {}\n".format(len(SucessCompat)))
    output.write("Fail app name: {}\n".format(len(FailCompat)))
    output.write("Uncover app name: {}\n".format(len(UncoverSet)))
    
    output.write("\n")
    output.write('------------------------- success details -----------------------------\n')
    for name in SucessCompat:
        output.write('   {}\n'.format(name))
    
    output.write("\n")
    output.write('------------------------- fail details -----------------------------\n')
    for name in FailCompat:
        output.write('   {}\n'.format(name))
        
    
    output.write("\n")
    output.write('------------------------- Uncover details -----------------------------\n')
    for name in UncoverSet:
        output.write('   {}\n'.format(name))
        
        
        
def prep_slot():
    for name in ApksToName.values():
        NameToSlot[name] = [0]*8
    
    

def hash(APIlevel):
    memo = {
        "API19":0, "API21":1, "API22":2, "API23":3, "API24":4, "API25":5,
        "API26":6, "API27":7
    }
    return memo[APIlevel]


def is_compatible(slot):
    return sum(slot) == 8
    
def multi_classify():
    # classification check for success lap range [19, 21-27] API
    for apk, name in ApksToName.items():
        for APIlevel, successApkSet in APIToSuccessApk.items():
            hash_idx = hash(APIlevel)
            if apk in successApkSet:
                # success at this API
                NameToSlot[name][hash_idx] = 1
    # Add the sucess apks
    for name, slot in NameToSlot.items():
        if is_compatible(slot):
            SucessCompat.add(name)

    # determine fail app if it is not success and have benn failed
    for apk, name in ApksToName.items():
        if name not in SucessCompat:
            for APIlevel, failApkSet in APIToFailureApk.items():
                if apk in failApkSet:
                   FailCompat.add(name)
                
    
    # add uncovered app name
    for apk, name in ApksToName.items():
        if name not in SucessCompat and name not in FailCompat:
            UncoverSet.add(name)
    

def helper_load(info, glbl_address):
    # Get the API level, followed only 2 digits for now.
    filename = glbl_address.upper()
    idx = filename.find("API")
    APIlevel = filename[idx:idx+5]

    paragraphs = info.split('\n\n')
    # as designed, thrid paragraph is the detailso of success
    detail_success = paragraphs[2].splitlines()

     
    # add success apk to that specific API key
    for line in detail_success:
        if line.startswith("----------"):
            continue 
        apkname = line.strip()
        APIToSuccessApk[APIlevel].add(apkname)
    
    # add fail apk to that sepefic API
    detail_fail = paragraphs[3].splitlines()
    for line in detail_fail:
        if line.startswith("Failure") or line.startswith("------------------------- details ---------------"):
            continue 
        apkname = line.strip()
        APIToFailureApk[APIlevel].add(apkname)
        
     
def load_result(result_dir):
    for parent, dirnames, filenames in os.walk(result_dir):
        for fname in filenames:
            glbl_address = os.path.join(parent, fname)
            f = open(glbl_address, 'r')
            info = f.read()
            f.close()
            helper_load(info, glbl_address)


def load_apkname(apkname_dir):
    for parent, dirnames, filenames in os.walk(apkname_dir):
        for fname in filenames:
            glbl_address = os.path.join(parent, fname)
            with open(glbl_address, newline="", errors="ignore") as csvfile:
                rows = csv.reader(csvfile)
                for row in rows:
                    apkname1 = row[0] + ".apk"
                    apkname2 = row[1] + ".apk"
                    apkname3 = row[2] + ".apk"
                    ApksToName[apkname1] = row[5]
                    ApksToName[apkname2] = row[5]
                    ApksToName[apkname3] = row[5]     
                    TotalNames.add(row[5])     
            csvfile.close()
    # prepare each apkname a 8 slots
    prep_slot()


if __name__ == "__main__":
    apkname_dir = sys.argv[1] 
    result_dir  = sys.argv[2]
    load_result(result_dir)
    load_apkname(apkname_dir)
    multi_classify()
    print_result()
