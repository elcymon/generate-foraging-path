import os
from glob import glob
#import ntpath
import pandas as pd

def waypoints2csv(waypointsDF):
    csvDF = pd.DataFrame(columns=['robot','targetModel'])
    
    robotID = None
    for idx,row in waypointsDF.iterrows():
        targetName = row.iloc[1]
        if 'robot' in targetName:
            robotID = int(targetName.replace('m_4wrobot',''))
            csvDF.loc[robotID,['robot','targetModel']] = [targetName,None]
            continue
        elif ('REUSE' in targetName) or ('End' in targetName):
            targetName = 'm_nest'
        elif 'Start' in targetName:
            continue
    
        if csvDF.loc[robotID,'targetModel'] is None:
           csvDF.loc[robotID,'targetModel'] = targetName
        else:
            csvDF.loc[robotID,'targetModel'] += ';' + targetName
    return csvDF

def process_waypoints(resultsPath,outputPath):
    os.makedirs(outputPath,exist_ok=True)
    
    for f in glob(resultsPath + '*.xy'):
        if '200' in f:
            print(f)
            df = pd.read_csv(f,sep='# ',header=None, engine='python')
            csvDF = waypoints2csv(df)
            csvName = f.replace(resultsPath,outputPath).replace('-200.xy','.csv')
            csvDF.to_csv(csvName,header=False,index=False)
if __name__ == '__main__':
    process_waypoints('results/','waypointsCSV/')