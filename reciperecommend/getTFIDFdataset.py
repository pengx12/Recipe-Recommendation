import pandas as pd
import numpy as np
def gettfidfdata(recipeid):
    sdf = pd.read_csv('sumdf.csv')
    for i in len(range(sdf.shape(0))):
        if sdf.iloc[i][0]=='recipeid':
            break
    if i >= sdf.shape(0):
        return None
    arr=[]
    index=i
    for i in len(range(sdf.shape(0))):
        #for j in len(range(sdf.shape(1))):
        #    if sdf.iloc[i][j]!=0 and sdf.iloc[index][j]!=0:
                s1=np.sqrt(sum(sdf.iloc[i][:]**2)+sum(sdf.iloc[index][:]**2))
                s2=sum(sdf.iloc[i][k]*sdf.iloc[index][k] for k in range(sdf.shape(1)))
                arr.put(((s2/s1),sdf.iloc[i][0]))
    arr.sort()
    return arr



