 
import pandas as pd
import numpy as np
import scipy.stats  as stats
allMetrics = "C:/Users/boxiang/Desktop/ResearchTask1/artifact/data/installforSPSS.xlsx" 
df = pd.read_excel(allMetrics, sheet_name='abi')
df_corr = pd.DataFrame() # Correlation matrix
df_p = pd.DataFrame()  # Matrix of p-values
for x in df.columns:
    for y in df.columns:
        corr = stats.spearmanr(df[x], df[y])
        df_corr.loc[x,y] = corr[0]
        df_p.loc[x,y] = corr[1]
        
print(df_corr)
 