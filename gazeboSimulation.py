# -*- coding: utf-8 -*-
import pandas as pd
pd.options.mode.chained_assignment = None
from glob import glob
import animateForagingStates
import animateForaging
import numpy as np

def loadDF(fname):
    robotDF,litterDF,nestDF = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    robots = []
    print(fname)
    expName = None
    for f in glob(fname):
        print(f)
        if 'litters' in f:
            litterDF = pd.read_csv(f,sep=',',index_col=0)
            
        elif 'robot' in f:
            robotDF = pd.read_csv(f,sep=',',index_col=0,header=[0, 1], skipinitialspace=True)
            expName = f.replace('.csv','')
            with open(f) as f1:
                robots = f1.readline().strip('\n').split(',')
                robots = [i for i in list(dict.fromkeys(robots)) if 'robot' in i]
        elif 'nest' in f:
            nestDF = pd.read_csv(f,sep=',',index_col=0)
    
    return expName,robotDF,litterDF.T,nestDF,robots

def toBoolean(x):
    x[x > 0] = True
    x[x < 1] = False
#    print(x.name)
    return x

def generateSimulationVideos():
    keys = pd.read_csv('icra2020/keys.csv')
    
    for i,k in keys.iterrows():
        print(f'{i+1} / {keys.shape[0]}')
        robotDF,litterDF,nestDF,robots = loadDF('icra2020/*' + k['t'] + '-*')
        litterDF.columns = list(litterDF.columns[0:2]) + list(robotDF.index)
        litterDF.iloc[:,2:] = litterDF.iloc[:,2:].apply(toBoolean)
        ani = animateForaging.animateForaging(robotDF,litterDF,nestDF,robots,worldXlength = 100, worldYlength = 100)
        ani.save('icra2020-sim-csv/' + k['world'] + '-' + k['algorithm'] + '-' + k['t'] + '-' + '.mp4')

def generateSimulationVideo(algorithm,t,world,filePath,worldXlength = 50, worldYlength = 50):
    robotsDF,litterDF,nestDF,robots = loadDF(filePath + '/*' + t + '*')
    print('loaded')
#    print(robotsDF.index)
    litterDF.columns = list(litterDF.columns[0:2]) + list(robotsDF.index)
    litterDF.iloc[:,2:] = litterDF.iloc[:,2:].astype(np.int).astype(np.bool)
    ani = animateForaging.animateForaging(robotsDF,litterDF,nestDF,robots,worldXlength = 50, worldYlength = 50)
    print('start animation')
    ani.save(filePath + '/' + world + '-' + t + '.mp4',fps=30)
    print('finished')
def icra2020SimVideos(folderPath):
    print(folderPath)
    algorithms = ['RW-s2s0p001-u2s0p1','RW-s2s0p001-u2s0p01']
    
#    ['N0-Q1-mSSD124','N0-Q1-mSSD220','N0-Q1-yolo3t128','N0-Q1-yolo3t224',
#     'N100-Q40-mSSD124','N100-Q40-mSSD220','N100-Q40-yolo3t128','N100-Q40-yolo3t224',
#     'RW-0p0025P-mSSD124','RW-0p0025P-mSSD220','RW-0p0025P-yolo3t128','RW-0p0025P-yolo3t224']
    
#        ['N0-Q1','N10-Q10','N100-Q40','RW-0p0025P','N100-Q1','N100-Q8',\
#                  'N100-Q20','N100-Q80','N100-Q120']
    for folder in glob(folderPath + '/*/'):
#        print(folder)
        if '100m' in folder:
            xlength = 100
            ylength = 100
        else:
            xlength = 50
            ylength= 50
        for alg in algorithms:
#            if alg in ['N100-Q40']:
#                continue
            print('\t',alg)
#            csvfile = f"{folder}{alg}*_{np.random.choice(np.arange(1,31,dtype=np.int)):03d}_*_*.csv"
            csvfile = f"{folder}{alg}*_001_*_*.csv"
            fname,robotsDF,litterDF,nestDF,robots = \
                loadDF(csvfile)
            if len(robots) == 0:
                continue
#            print('robots',robotsDF.shape)
#            print('litter',litterDF.shape)
            litterDF.columns = list(litterDF.columns[0:2]) + list(robotsDF.index)
            litterDF.iloc[:,2:] = litterDF.iloc[:,2:].astype(np.int).astype(np.bool)
            ani = animateForagingStates.animateForagingStates(robotsDF,litterDF,nestDF,robots,worldXlength = xlength, worldYlength = ylength)
            ani.save(fname + '.mp4',fps=30,dpi=300,)
            
if __name__ == '__main__':
    folderPath = '/home/elcymon/containers/swarm_sim/results/model-s2s-u2s'#'icra2020/simVideos'
    icra2020SimVideos(folderPath)
#    generateSimulationVideos()
