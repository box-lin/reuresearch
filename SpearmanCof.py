import pandas as pd
import numpy as np
import scipy.stats  as stats

"""_Excel address_
"""
InbenignDir = "SSPS/A-BenignInstallforSPSS.xlsx"   #1-Total, 2-abi, 3-library 
RunbenignDIr = "SSPS/A-BenignRuntimeforSPSS.xlsx"  #1-total, 4-native, 5-verify
InmalwareAllDir = "SSPS/malwareInstallTable.xlsx"
InmalwareABIDir = "SSPS/malwareInstallTableABI.xlsx"
InmalwareLibDir = "SSPS/malwareInstallTableLibrary.xlsx"
RunmalwareAllDir = "SSPS/malwareRuntimeTable.xlsx"
RunmalwareNatDIr = "SSPS/malwareRuntimeTableNative.xlsx"
RunmalwareVerDir = "SSPS/malwareRuntimeTableVerify.xlsx"


"""_Read Excels and compute correlation_
"""
def printCorr(dir, sheetName=None):
    print("=================================", dir, sheetName, "======================================")
    if sheetName:
        df = pd.read_excel(dir, sheet_name=sheetName)
    else:
        df = pd.read_excel(dir)
    df_corr = pd.DataFrame() # Correlation matrix
    for x in df.columns:
        for y in df.columns:
            corr = stats.spearmanr(df[x], df[y])
            df_corr.loc[x,y] = corr[0]   
    print(df_corr)
    print("")

printCorr(InbenignDir, 'Total')
printCorr(InbenignDir, 'abi')
printCorr(InbenignDir, 'library')
printCorr(RunbenignDIr, 'total(all)')
printCorr(RunbenignDIr, 'native')
printCorr(RunbenignDIr, 'verify')
printCorr(InmalwareAllDir)
printCorr(InmalwareABIDir)
printCorr(InmalwareLibDir)
printCorr(RunmalwareAllDir)
printCorr(RunmalwareNatDIr)
printCorr(RunmalwareVerDir)




