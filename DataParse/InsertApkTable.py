"""
    This file insert the 
    
    I) apk table columns 
            1. apkname varchar
            2. typ varchar
            3. apkyear varchar
            4. apkapi varchar
            5. apiyear varchar 
    
    II) apkruncompat table columns
            1. apkname varchar
            2. typ varchar
            3. isFail boolean
            4. runMsg varchar 
            
    III) apkinscompat table columns
            1. apkname varchar
            2. typ varchar
            3. isFail boolean 
            4. runMsg varchar
""" 
import psycopg2
import os
import os.path
import re
import sys
 

def get_apkapi(fname_lower)->str:
    api_idx = fname_lower.find("api")
    apkapi = fname_lower[api_idx+3:api_idx+5]
    return apkapi

def get_apktyp(fname_lower)->str:
    keywords = {'benign', 'malware'}
    for word in keywords:
        if fname_lower.find(word) >= 0 :
            return word
    return"Notyp" #this is impossible

def get_apkyear(fname_lower)->str: 
    keywords = set()
    for i in range(2010, 2020):
        keywords.add(str(i))
    for word in keywords:
        if fname_lower.find(word) >= 0:
            return word 
    return "Noyear"


def get_apiyear(apiyear):
    dic = {"19":"2013", "20":"2014", "21":"2014", "22":"2015", "23":"2015", "24":"2016",
           "25": "2016", "26": "2017", "27": "2017", "28":"2018"}
    return dic[apiyear] # impossible keyerror

 # inner helper function
def apkcol_collect(info, fname_lower):
    # these can be obtain from filename
    apkapi = get_apkapi(fname_lower)
    typ = get_apktyp(fname_lower)
    apkyear = get_apkyear(fname_lower)
    
    # apiyear can be obtain by hard coded.
    apiyear = get_apiyear(apkapi)
    
    lst = info.splitlines()
    for line in lst:
        row = line.strip()
        # start inserting
        if row.find('apk') >= 10:
            apkdata[(row,typ)] = [apkyear, apkapi, apiyear]
            
def collect_apk(path):   
    for parent,dirnames, filenames in os.walk(path):
        for fname in filenames:
            fname_lower = fname.lower() 
            address = os.path.join(parent,fname)   
            # read the txt
            f = open(address, 'r')
            info = f.read()
            f.close()
            apkcol_collect(info, fname_lower)

def insert_apkdata():
     # after collect all info insert. Doing this so badly because theres lot of same apk in multiple API? why!!
    for key, lst in apkdata.items():
        apkname, typ = key
        try:
            cur.execute("INSERT into apk(apkname, typ, apkyear, apkapi, apiyear)"
                        + " VALUES (%s, %s, %s, %s, %s)", 
                        (apkname, typ, lst[0], lst[1], lst[2]))
        except Exception as e:
            print("Insert to apk table failed!",e)
            return
        conn.commit()


def collect_ins_success(data, typ):
    listlines = data.splitlines()
    if len(listlines) <= 1: return 
    for apknamestr in listlines[1:]:
        apkname = apknamestr.strip()
        # [isfail, msg]
        apkins_compat[(apkname, typ)] = [False, "N/A"]

def collect_ins_fail(data, typ):
    listlines = data.splitlines()
    if len(listlines) <= 1: return  
    curfailmsg = ""
    for row in listlines[1:]:
        if row.startswith('Failure'):
            lst = row.split()
            curfailmsg = lst[1][1:-2]
        else:
            apkname = row.strip()
            apkins_compat[(apkname, typ)] = [True, curfailmsg]

def collect_ins_compat(info, fname_lower):
    paragraphs = info.split('\n\n')
    typ = get_apktyp(fname_lower)
    collect_ins_success(paragraphs[2], typ)
    collect_ins_fail(paragraphs[3], typ)


def collect_run_success(data, typ):
    listlines = data.splitlines()
    if len(listlines) <= 1: return 
    for apknamestr in listlines[1:]:
        apkname = apknamestr.strip()
        # [isfail, msg]
        apkrun_compat[(apkname, typ)] = [False, "N/A"]
        
def collect_run_fail(data, typ):
    listlines = data.splitlines()
    if len(listlines) <= 1: return  
    curfailmsg = ""
    for row in listlines[1:]:
        if row.startswith('Failure'):
            lst = row.split()
            curfailmsg = lst[1][1:-2]
        else:
            apkname = row.strip()
            apkrun_compat[(apkname, typ)] = [True, curfailmsg]

def collect_run_compat(info, fname_lower):
    paragraphs = info.split('\n\n')
    typ = get_apktyp(fname_lower)
    collect_run_success(paragraphs[2], typ)
    collect_run_fail(paragraphs[3], typ)
    
def collect_compat(path):
    for parent,dirnames, filenames in os.walk(path):
        for fname in filenames:
            fname_lower = fname.lower() 
            address = os.path.join(parent,fname)   
            # read the txt
            f = open(address, 'r')
            info = f.read()
            f.close()
            collect_ins_compat(info, fname_lower)
            collect_run_compat(info, fname_lower)


def insert_compat():
    for key, lst in apkins_compat.items():
        apkname, typ = key 
        # since this is sub enetity
        if key in apkdata:
            try:
                cur.execute("INSERT into apkinscompat(apkname, typ, ins_fail, insMsg)"
                            + " VALUES (%s, %s, %s, %s)", 
                            (apkname, typ, lst[0], lst[1]))
            except Exception as e:
                print("Insert to apk table failed!",e)
                return
            conn.commit()
    
    for key, lst in apkrun_compat.items():
        apkname, typ = key 
        if key in apkdata:
            try:
                cur.execute("INSERT into apkruncompat(apkname, typ, run_fail, runMsg)"
                            + " VALUES (%s, %s, %s, %s)", 
                            (apkname, typ, lst[0], lst[1]))
            except Exception as e:
                print("Insert to apk table failed!",e)
                return
            conn.commit() 

def void_main():
    # just hardcode the path
    inspath = "../InstallResult"
    runpath = "../RuntimeResult"
    collect_apk(inspath)
    collect_apk(runpath)
    
    # insert_apkdata()
    
    collect_compat(inspath) 
    collect_compat(runpath) 
    insert_compat()

def db_connect():
    conn = None
    try:
        conn = psycopg2.connect(dbname = "reu", user = "postgres", host = "localhost", password = "123456", port = "5432")
    except:
        print('Unable to connect to the database!')
    cur = conn.cursor()
    return cur, conn

def db_close(cur, conn):
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    # glbl variables
    cur, conn = db_connect()
    apkdata = {}
    apkins_compat = {}
    apkrun_compat ={}
    void_main()
    db_close(cur, conn)