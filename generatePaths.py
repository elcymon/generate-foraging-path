# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re

def loadInitialState(stateCSV):
    csvdf = pd.read_csv(stateCSV,sep=',')
    csvdf.index = csvdf['name']
    
    robots = csvdf[csvdf['name'].str.contains('robot')]['name']
    xyYaw = np.append(csvdf.loc[:,'x':'yaw'].columns.values,['litterCount'])
    robotDFcolumns = pd.MultiIndex.from_product([robots,xyYaw],names=['names','pose'])
    robotsDF = pd.DataFrame(columns=robotDFcolumns)
    robotsDF.index.name = 'time'
    t = 0
    for i in robots:
        robotsDF.loc[t,i] = np.append(csvdf.loc[i,'x':'yaw'].values,[0])

    littersDF = csvdf[csvdf['name'].str.contains('litter')].copy()
    littersDF.loc[:,t] = True
    littersDF.drop(columns = ['name','yaw'], inplace = True)
    littersDF.columns.name = 'poseNtime'
    
    nestDF = pd.DataFrame([0],columns=['litterCount'],index=[0])
    nestDF.index.name = 'time'
    return robotsDF,littersDF,nestDF#robots,xyYaw#csvdf #initialState

def loadforagingWayPoints(wayPointsFile):
    wayPointsDict = {}
    robot = None
    with open(wayPointsFile, 'r') as f:
        for row in f:
            
            row = row.strip('\n').replace('#',' ')
            row = re.split('\s+',row)
            if len(row) > 1:
                if 'robot' in row[-1]:
                    robot = row[-1]
                    wayPointsDict[robot] = []
                elif robot != None and len(row) == 3:
                    wayPointsDict[robot].append([float(row[0]), float(row[1]), row[2]])
                        
            #print(row)
    
    return wayPointsDict


def computeRobotStep(robotData,robotGoal,moveDistance):
    goalx,goaly,activity = robotGoal
    
    #compute distance from goal
    distanceFromGoal = np.linalg.norm([goalx, goaly], [robotData['x'], robotData['y']])
    #compute orientation of goal from location
    
    if distanceFromGoal > moveDistance:
        movementY = np.sin(robotData['yaw']) * moveDistance
        movementX = np.cos(robotData['yaw']) * moveDistance
    else:#distance of time step will go past goal
        # goto goal location
        robotData['x'] = goalx
        robotData['y'] = goaly
        
        #execute activity
        
        #compute new heading
        
        #compute new location of robot
        movementY = np.sin(robotData['yaw']) * (moveDistance - distanceFromGoal)
        movementX = np.cos(robotData['yaw']) * (moveDistance - distanceFromGoal)
    
        
    
    return newRobotData
#robotsDF,littersDF,nestDF = loadInitialState('CSVresults/20180208_w_swarm1_circular_one_region_cluster.csv')
foragingWayPointsDF = loadforagingWayPoints('results/one_region_cluster-200.xy')