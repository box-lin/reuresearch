import os
import Utils
import collections
import csv 

def collectAppsPerYear(apkNameDir, installDir, runtimeDir):
    """_Serve for RQ1_

    Args:
        apkNameDir (_str_): _directory for csv files_
        installDir (_str_): _directory for installResult_
        runtimeDir (_str_): _directory for runtimeResult_

    Returns:
        _dic_: _at given year key and type: set of app name_
        _dic_: _at given typ and apk and year: its app name
        
    """
    # {(year typ): {appname, .....}}
    yearApps = collections.defaultdict(set) 
    yearAPIapps = collections.defaultdict(set) 
    totalApps = {}
    for parent, dirnames, filenames in os.walk(apkNameDir):
        for fname in filenames:
            apkToApp = {} 
            glbl_address = os.path.join(parent, fname)
            appTyp = Utils.getType(glbl_address.lower())
            appYear = Utils.getYear(glbl_address.lower())
            with open(glbl_address, newline="", errors="ignore") as csvfile:
                rows = csv.reader(csvfile)
                for row in rows:
                    apkname1 = row[0] + ".apk"
                    apkname2 = row[1] + ".apk"
                    apkname3 = row[2] + ".apk"
                    apkToApp[apkname1] = row[5]
                    apkToApp[apkname2] = row[5]
                    apkToApp[apkname3] = row[5]    
                    
                    totalApps[(apkname1, appYear, appTyp)] = row[5]
                    totalApps[(apkname2, appYear, appTyp)] = row[5]
                    totalApps[(apkname3, appYear, appTyp)] = row[5] 
            csvfile.close()
            
            # RQ2
            yearStr = Utils.getYear(fname.lower())
            # api2Apks = Utils.getApi2Apks(installDir, yearStr, appTyp)
            api2Apks = Utils.getApi2Apks2(installDir, yearStr)
            for api, apkSet in api2Apks.items():
                appNameSet = set()
                for apk in apkSet:
                    if apk in apkToApp.keys():
                        curAppName = apkToApp[apk]
                        appNameSet.add(curAppName)
                yearAPIapps[(yearStr, appTyp, api)] |= appNameSet
            
            # RQ1
            # search on installDir, runtimeDir for all apks and find its app according to table apkToApp
            appset1 = Utils.searchAdd2AppSet(installDir, yearStr, apkToApp)
            appset2 = Utils.searchAdd2AppSet(runtimeDir, yearStr, apkToApp)
            yearApps[(yearStr, appTyp)] |= appset1
            yearApps[(yearStr, appTyp)] |= appset2

    return yearApps, totalApps, yearAPIapps

def multiCompatCollect(yearsApps, installDir, runtimeDir, totalApps):
    installMulti = {}
    runMulti = {}
    for key, appSet in yearsApps.items():  
        year, typ = key           
                                                                        #            19 21 .... API levels maps
        installCompatSlot = { app:[0]*8 for app in appSet}              #[appName :  [0,0,0,0,0,0,0]] 
        runCompatSlot = { app:[0]*8 for app in appSet} 
        API2SuccessApkInstall = Utils.getApi2Apks(installDir, year, typ)
        API2SuccessApkRuntime = Utils.getApi2Apks(runtimeDir, year, typ)
        
        for apiLevel, successApks in API2SuccessApkInstall.items():
            apiIndex = Utils.hash(apiLevel)
            for apk in successApks:
                appName = totalApps[(apk, year, typ)]
                installCompatSlot[appName][apiIndex] = 1
        
        for apiLevel, successApks in API2SuccessApkRuntime.items():
            apiIndex = Utils.hash(apiLevel)
            for apk in successApks:
                appName = totalApps[(apk, year, typ)]
                runCompatSlot[appName][apiIndex] = 1
            
        installMulti[key] = installCompatSlot
        runMulti[key] = runCompatSlot
    
    return installMulti, runMulti 

def printRQ1(yearsApps):
    print("========================== RQ1 data: ===============================")
    for key, apps in yearsApps.items():
        print(key, " numbers of apps: ", len(apps))
        
def printRQ2(yearAPIapps):
    print("========================== RQ2 data: ===============================")
    for key, apps in yearAPIapps.items():
        print(key, " numbers of apps: ", len(apps))
        
        
def printRQ3(installMulti, runMulti):
    print("========================== RQ3 data: ===============================")
    for key, dic in installMulti.items(): #very tiny
        for coverage in range(9):         #very tiny as well
            cnt = 0
            for app, slotList in dic.items(): 
                cover = sum(slotList)
                if coverage == cover: cnt += 1
            print(key, 'Installation Coverage At', str(coverage) +'/8: ', cnt)
            
    for key, dic in runMulti.items(): #very tiny
        for coverage in range(9):         #very tiny as well
            cnt = 0
            for app, slotList in dic.items(): 
                cover = sum(slotList)
                if coverage == cover: cnt += 1
            print(key, 'Runtime Coverage At', str(coverage) +'/8: ', cnt)
                    
                    
def main():
    installDir, runtimeDir = '../InstallResult', '../RuntimeResult'
    apkNameDir = 'C:/Users/boxiang/Desktop/ResearchTask1/apkname/'
    yearsApps, totalApps, yearAPIapps = collectAppsPerYear(apkNameDir, installDir, runtimeDir)
    printRQ1(yearsApps)
    printRQ2(yearAPIapps)
    installMulti, runMulti = multiCompatCollect(yearsApps, installDir, runtimeDir, totalApps)
    printRQ3(installMulti, runMulti)
    
    

if __name__ == "__main__":
    main()