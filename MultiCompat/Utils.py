import collections
import os

def getType(fname_lower):
    keywords = {'benign', 'malware'}
    for word in keywords:
        if fname_lower.find(word) >= 0 :
            return word
    return"Notyp" #this is impossible

def getYear(fname_lower)->str: 
    keywords = set()
    for i in range(2010, 2020):
        keywords.add(str(i))
    for word in keywords:
        if fname_lower.find(word) >= 0:
            return word 
    return "Noyear"

def getApi(fname_lower)->str:
    api_idx = fname_lower.find("api")
    apkapi = fname_lower[api_idx+3:api_idx+5]
    return apkapi

def hash(APIlevel):
    memo = {
        "19":0, "21":1, "22":2, "23":3, "24":4, "25":5,
        "26":6, "27":7
    }
    return memo[APIlevel]
 


def isCompatible(slot):
    return sum(slot) == 8


def initSlot(ApksToName):
    NameToSlot = collections.defaultdict(list)
    for name in ApksToName.values():
        NameToSlot[name] = [0]*8
    return NameToSlot


def addApkToList(apkList, page):
    fnamelower = page.splitlines()[0].lower()
    apkYear = getYear(fnamelower)
    
    # only focuses on 2018 and 2019
    if apkYear != '2018' and apkYear != '2019': return
    
    typ = getYear(fnamelower)
    apkAPI = getApi(fnamelower)
    paragraphs = page.split('\n\n')
    
    for paragraph in paragraphs[2:]:
        lines = paragraph.splitlines()
        for line in lines:
            if line.find('apk') >= 0:
                apkNum = line.strip()
                apkItem = Apk(apkNum, apkYear, apkAPI, typ)
                apkList.append(apkItem)
    
 

def searchAdd2AppSet(dir, yearStr, apkToApp):
    appSet = set()
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            glbl_address = os.path.join(parent, fname)
            f = open(glbl_address, 'r')
            info = f.read()
            f.close()
            fnameLower = fname.lower()
            curYear = getYear(fnameLower)
            
            if curYear != yearStr:
                continue 
            
            paragraphs = info.split('\n\n')
            for paragraph in paragraphs[2:]:
                lines = paragraph.splitlines()
                for line in lines:
                    if line.find('apk') >= 0:
                         apkname = line.strip()
                         if apkname in apkToApp.keys():
                            appname = apkToApp[apkname]
                            appSet.add(appname)
    return appSet


# only puck success
def getApi2Apks(dir, year, typ):
    api2apks = collections.defaultdict(set)
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            glbl_address = os.path.join(parent, fname)
            fnameLower = fname.lower()
            apkYear = getYear(fnameLower)
            apkTyp = getType(fnameLower)
            if apkYear == year and apkTyp == typ:
                f = open(glbl_address, 'r')
                info = f.read()
                f.close()
                apiLevel = getApi(fnameLower)
                paragraphs = info.split('\n\n')
                for line in paragraphs[2].splitlines():
                    if line.startswith("----------"):
                        continue 
                    apkname = line.strip()
                    api2apks[apiLevel].add(apkname)
    return api2apks

# pick success and fail
def getApi2Apks2(dir, year):
    api2apks = collections.defaultdict(set)
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            glbl_address = os.path.join(parent, fname)
            fnameLower = fname.lower()
            apkYear = getYear(fnameLower)
            apkTyp = getType(fnameLower)
            if apkYear == year:
                f = open(glbl_address, 'r')
                info = f.read()
                f.close()
                apiLevel = getApi(fnameLower)
                paragraphs = info.split('\n\n')
                for paragraph in paragraphs[2:]:
                    lines = paragraph.splitlines()
                    for line in lines:
                        if line.find('apk') >= 0:
                            apkname = line.strip()
                            api2apks[apiLevel].add(apkname)
    return api2apks