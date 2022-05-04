from Utils import SPSSutil
import os
import os.path


"""_update the table for success count immidiately per given txt read _
"""
def updateSuccess(fname_lower, minSdkDic, table, data):
    # just in case paragraph exists only the header, return immidiately 
    listlines = data.splitlines()
    if len(listlines) <= 1: return 
    
    # get the identities
    apkyear = SPSSutil.get_apkyear(fname_lower)
    apilevel = SPSSutil.get_apkapi(fname_lower)
    typ = SPSSutil.get_apktyp(fname_lower)
    apiyear = SPSSutil.get_apiyear(apilevel)
    
    # traverse through the success apks
    for apknamestr in listlines[1:]:
        apkname = apknamestr.strip()
        # generate the tuple key so to get the min sdk from minSdkDic
        tupkey = (apkname, apkyear, typ)
        if tupkey in minSdkDic.keys():
            minSdkVersion = minSdkDic[tupkey]
            #(minsdk, api, apkyear, apiyear) is the key for table
            # and [#success, #fail] is the value for table.
            # Now, update the table
            tableKey = (minSdkVersion, apilevel, apkyear, apiyear)
            table[tableKey][0] += 1
            
"""_update the table for fail count immidiately per given txt read _
"""
def updateFail(fname_lower, minSdkDic, table, data):
    # just in case paragraph exists only the header, return immidiately 
    listlines = data.splitlines()
    if len(listlines) <= 1: return 
    
    # get the identities
    apkyear = SPSSutil.get_apkyear(fname_lower)
    apilevel = SPSSutil.get_apkapi(fname_lower)
    typ = SPSSutil.get_apktyp(fname_lower)
    apiyear = SPSSutil.get_apiyear(apilevel)
    
    for row in listlines[1:]:
        if row.startswith('Failure'):
            continue
        else:
            apkname = row.strip()
            tupkey = (apkname, apkyear, typ)
            if tupkey in minSdkDic.keys():
                minSdkVersion = minSdkDic[tupkey]
                tableKey = (minSdkVersion, apilevel, apkyear, apiyear)
                table[tableKey][1] += 1

"""_update the table for target fail count immidiately per given txt read_
"""
def updateTargetFail(fname_lower, minSdkDic, table, data, failMsg):
    # just in case paragraph exists only the header, return immidiately 
    listlines = data.splitlines()
    if len(listlines) <= 1: return 
    
    # get the identities
    apkyear = SPSSutil.get_apkyear(fname_lower)
    apilevel = SPSSutil.get_apkapi(fname_lower)
    typ = SPSSutil.get_apktyp(fname_lower)
    apiyear = SPSSutil.get_apiyear(apilevel)
    
    flag = False 
    for row in listlines[1:]:
        if row.startswith('Failure'):
            curfailmsg = row.split()[1][1:-2]
            if curfailmsg == failMsg:
                flag = True
            else:
                flag = False 
        elif flag:
            apkname = row.strip()
            tupkey = (apkname, apkyear, typ)
            if tupkey in minSdkDic.keys():
                minSdkVersion = minSdkDic[tupkey]
                tableKey = (minSdkVersion, apilevel, apkyear, apiyear)
                table[tableKey][1] += 1
            
            
def updateTable(logPath, minSdkDic, table, typ, failMsg=None):
    for parent,dirnames, filenames in os.walk(logPath):
        for fname in filenames:
            fname_lower = fname.lower()
            # dont consider other logs other than the requested typ
            if fname_lower.find(typ) < 0: continue
            
            # read the current pointed text
            address = os.path.join(parent,fname)  
            f = open(address, 'r')
            info = f.read()
            f.close()
            
            # per design of txt format we can locate the success apks and failure apks quickly
            # by divide the txt to paragraphs
            paragraphs = info.split('\n\n')
            sucessPara = paragraphs[2]
            failPara = paragraphs[3]
            
            # do the general updates, this is to original tables
            if not failMsg:
                updateSuccess(fname_lower, minSdkDic, table, sucessPara)
                updateFail(fname_lower, minSdkDic, table, failPara)
            else:
                # with specific msg given.
                updateTargetFail(fname_lower, minSdkDic, table, failPara, failMsg)

def void_main():
    """ApkSdkDic[(apkname, apkyear, typ)] = minSdkVersion
    """
    malwareMinSdkDic = SPSSutil.get_minSDK_dic("DataParse/malware-minsdk")
    benignMinSdkDic = SPSSutil.get_minSDK_dic("DataParse/benign-minsdk(2018-2019)")
    
    """SSPS tables, get_dic() return a dictionary with apk year 2018-2019
                  , get_dic_full() return a dictionary with apk year 2010-2019
    """
    benignInstallTable = SPSSutil.get_dic()
    benignRuntimeTable = SPSSutil.get_dic()
    malwareInstallTable = SPSSutil.get_dic()
    malwareRuntimeTable = SPSSutil.get_dic_full()
    
    """Update the above tables for SSPS
    """
    updateTable("InstallResult", benignMinSdkDic, benignInstallTable, "benign")
    updateTable("RuntimeResult", benignMinSdkDic, benignRuntimeTable, "benign")
    updateTable("InstallResult", malwareMinSdkDic, malwareInstallTable, "malware")
    updateTable("RuntimeResult", malwareMinSdkDic, malwareRuntimeTable, "malware")
    
    SPSSutil.originalTableWrite2Excel(benignInstallTable, "SSPS/benignInstallTable.xlsx")
    SPSSutil.originalTableWrite2Excel(benignRuntimeTable, "SSPS/benignRuntimeTable.xlsx")
    SPSSutil.originalTableWrite2Excel(malwareInstallTable, "SSPS/malwareInstallTable.xlsx")
    SPSSutil.originalTableWrite2Excel(malwareRuntimeTable, "SSPS/malwareRuntimeTable.xlsx")
    
    
    """Now focuse on specific type of failures, define msgs and transform tables
       now the below tables with value = [total, 0]
    """ 
    abiMsg = "INSTALL_FAILED_NO_MATCHING_ABIS"
    libraryMsg = "INSTALL_FAILED_MISSING_SHARED_LIBRARY"
    verifyMsg = "java.lang.VerifyError"
    nativeMsg = "Native"    
    
    benignInstallTableABI = SPSSutil.transform(benignInstallTable)
    benignInstallTableLibrary = SPSSutil.transform(benignInstallTable)
    benignRuntimeTableVerify = SPSSutil.transform(benignRuntimeTable)
    benignRuntimeTableNative = SPSSutil.transform(benignRuntimeTable)
    malwareInstallTableABI = SPSSutil.transform(malwareInstallTable)
    malwareInstallTableLibrary = SPSSutil.transform(malwareInstallTable)
    malwareRuntimeTableVerify = SPSSutil.transform(malwareRuntimeTable)
    malwareRuntimeTableNative = SPSSutil.transform(malwareRuntimeTable)
     
    updateTable("InstallResult", benignMinSdkDic, benignInstallTableABI, "benign", abiMsg)
    updateTable("InstallResult", benignMinSdkDic, benignInstallTableLibrary, "benign", libraryMsg)
    updateTable("RuntimeResult", benignMinSdkDic, benignRuntimeTableVerify, "benign", verifyMsg)
    updateTable("RuntimeResult", benignMinSdkDic, benignRuntimeTableNative, "benign", nativeMsg)
    
    updateTable("InstallResult", malwareMinSdkDic, malwareInstallTableABI, "malware", abiMsg)
    updateTable("InstallResult", malwareMinSdkDic, malwareInstallTableLibrary, "malware", libraryMsg)
    updateTable("RuntimeResult", malwareMinSdkDic, malwareRuntimeTableVerify, "malware", verifyMsg)
    updateTable("RuntimeResult", malwareMinSdkDic, malwareRuntimeTableNative, "malware", nativeMsg)
    
    
    SPSSutil.specificTableWrite2Excel(benignInstallTableABI, "SSPS/benignInstallTableABI.xlsx")
    SPSSutil.specificTableWrite2Excel(benignInstallTableLibrary, "SSPS/benignInstallTableLibrary.xlsx")
    SPSSutil.specificTableWrite2Excel(benignRuntimeTableVerify, "SSPS/benignRuntimeTableVerify.xlsx")
    SPSSutil.specificTableWrite2Excel(benignRuntimeTableNative, "SSPS/benignRuntimeTableNative.xlsx")
    SPSSutil.specificTableWrite2Excel(malwareInstallTableABI, "SSPS/malwareInstallTableABI.xlsx")
    SPSSutil.specificTableWrite2Excel(malwareInstallTableLibrary, "SSPS/malwareInstallTableLibrary.xlsx")
    SPSSutil.specificTableWrite2Excel(malwareRuntimeTableVerify, "SSPS/malwareRuntimeTableVerify.xlsx")
    SPSSutil.specificTableWrite2Excel(malwareRuntimeTableNative, "SSPS/malwareRuntimeTableNative.xlsx")


if __name__ == "__main__":
    void_main()
