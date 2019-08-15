# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from scipy.spatial.distance import euclidean

def loadInitialState(stateCSV):
    csvdf = pd.read_csv(stateCSV,sep=',')
    csvdf.index = csvdf['name']
    
    robots = csvdf[csvdf['name'].str.contains('robot')]['name']
    xyYaw = np.append(csvdf.loc[:,'x':'yaw'].columns.values,['litterCount'])
    robotDFcolumns = pd.MultiIndex.from_product([robots,xyYaw],names=['names','pose'])
    robotsDF = pd.DataFrame(columns=robotDFcolumns)
    robotsDF.index.name = 'time'
    t = str(0)
    for i in robots:
        robotsDF.loc[t,i] = np.append(csvdf.loc[i,'x':'yaw'].values,[0])

    littersDF = csvdf[csvdf['name'].str.contains('litter')].copy()
    littersDF.loc[:,t] = True
    littersDF.drop(columns = ['name','yaw'], inplace = True)
    littersDF.columns.name = 'poseNtime'
    
    nestDF = pd.DataFrame([0],columns=['litterCount'],index=[t])
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


def computeRobotStep(robotData,robotWayPoints,moveDistance):
    goalx,goaly,activity = robotWayPoints[0]
#    print(goalx,goaly,robotData['x'],robotData['y'])
    #compute distance from goal
    distanceFromGoal = euclidean([goalx, goaly], [robotData['x'], robotData['y']])
    
    if distanceFromGoal > moveDistance:
        movementY = np.sin(robotData['yaw']) * moveDistance
        movementX = np.cos(robotData['yaw']) * moveDistance
    else:#distance of time step will go past goal
        # goto goal location
        robotData['x'] = goalx
        robotData['y'] = goaly
        robotWayPoints.pop(0)#pop current goal to move to next goal
        #execute activity
#        if 'litter' in activity:
#            #pick up the particular litter and update littersDF
#        elif 'reuse' in activity.tolower() or 'end' in activity.tolower():
            #drop off all litter foraged and update the time step in nestDF
        
        #compute new heading:  get next goal ie waypoint
        if len(robotWayPoints) > 0: #no more waypoints for the robot
            goalx,goaly,activity = robotWayPoints[0]
            robotData['yaw'] = np.arctan2(goaly - robotData['y'], goalx - robotData['x'])
            #compute new location of robot
            movementY = np.sin(robotData['yaw']) * (moveDistance - distanceFromGoal)
            movementX = np.cos(robotData['yaw']) * (moveDistance - distanceFromGoal)
        else:
            movementX = 0
            movementY = 0
    robotData['x'] += movementX
    robotData['y'] += movementY
        
    
    return robotData,robotWayPoints

robotsDF,littersDF,nestDF = loadInitialState('CSVresults/20180208_w_swarm1_circular_one_region_cluster.csv')
foragingWayPointsDF = loadforagingWayPoints('results/one_region_cluster-200.xy')
t = 0
timeStep = 1 # second
robotVelocity = 0.605 #metres/seconds
moveDistance = robotVelocity * timeStep # distance is velocity x time
while t < 100:
    for robot in foragingWayPointsDF.keys():
        robotData = robotsDF.loc[str(t),robot]
        robotWayPoints = foragingWayPointsDF[robot]
#        if t == 0:#remove start location for robot at initial time step
#            robotWayPoints.pop(0)
        if len(robotWayPoints) > 0:
            robotData,robotWayPoints = computeRobotStep(robotData,robotWayPoints,moveDistance)
            robotsDF.loc[str(round(t+timeStep,1)),robot] = robotData.values
#            print(robotData)
#            print(robotsDF.loc[str(t+timeStep),robot])
        else:
            robotsDF.loc[str(round(t+timeStep,1)),robot] = robotData.values
    #increase time 
    t = round(t + timeStep,1)
    
    print(t)
        