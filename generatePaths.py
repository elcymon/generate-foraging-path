# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
from glob import glob
import animateForaging
import ntpath

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
    
    nestDF = pd.DataFrame(np.array([[0,0]]),columns=['litterCount','tPlusProcessing'],index=[t])
    nestDF.index.name = 'time'
    return robotsDF,littersDF,nestDF#robots,xyYaw#csvdf #initialState

def loadforagingWayPointsAndWaitingTimes(wayPointsFile):
    wayPointsDict = {}
    robotsWaitingTime = {}
    robot = None
    with open(wayPointsFile, 'r') as f:
        for row in f:
            
            row = row.strip('\n').replace('#',' ')
            row = re.split('\s+',row)
            if len(row) > 1:
                if 'robot' in row[-1]:
                    robot = row[-1]
                    wayPointsDict[robot] = []
                    robotsWaitingTime[robot] = 0
                elif robot != None and len(row) == 3:
                    wayPointsDict[robot].append([float(row[0]), float(row[1]), row[2]])
                        
            #print(row)
    
    return wayPointsDict,robotsWaitingTime


def computeRobotStep(robotData,robotWayPoints,moveDistance):
    goalx,goaly,activity = robotWayPoints[0]
    action = None
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
        action = activity
#        if 'litter' in activity:
#            #pick up the particular litter and update littersDF
#        elif 'reuse' in activity.tolower() or 'end' in activity.tolower():
            #drop off all litter foraged and update the time step in nestDF
        
        #compute new heading:  get next goal ie waypoint
        if len(robotWayPoints) > 0: #no more waypoints for the robot
            goalx,goaly,_ = robotWayPoints[0]
            robotData['yaw'] = np.arctan2(goaly - robotData['y'], goalx - robotData['x'])
            #compute new location of robot
            movementY = np.sin(robotData['yaw']) * (moveDistance - distanceFromGoal)
            movementX = np.cos(robotData['yaw']) * (moveDistance - distanceFromGoal)
        else:
            movementX = 0
            movementY = 0
    robotData['x'] += movementX
    robotData['y'] += movementY
        
    
    return robotData,robotWayPoints,action


def simulateForagingAndSaveResults(initialWorldStateFile,wayPointsFile,timeStep,litProcessingTime,robotVelocity):
    robotsDF,littersDF,nestDF = loadInitialState('CSVresults/' + initialWorldStateFile)
    foragingWayPointsDF,robotsWaitingTime = loadforagingWayPointsAndWaitingTimes('results/' + wayPointsFile)
    t = 0
    moveDistance = robotVelocity * timeStep # distance is velocity x time
    while True:
        #copy previous state of litter available and litter deposited in nest to default of current state
        tStr = str(round(t,1))
        tPlus1 = str(round(t + timeStep, 1))
        littersDF.loc[:,tPlus1] = littersDF.loc[:,tStr].values
        nestDF.loc[tPlus1,'litterCount'] = nestDF.loc[tStr,'litterCount']
        nestDF.loc[tPlus1,'tPlusProcessing'] = nestDF.loc[tStr,'tPlusProcessing'] + timeStep
        numRobotsFinishedWayPoints = 0
    
        for robot in foragingWayPointsDF.keys():
            action = None
            robotData = robotsDF.loc[tStr,robot]
            robotWayPoints = foragingWayPointsDF[robot]
    #        if t == 0:#remove start location for robot at initial time step
    #            robotWayPoints.pop(0)
            if len(robotWayPoints) > 0 and robotsWaitingTime[robot] <= 0:
                robotsWaitingTime[robot]  = 0 # by default robot does not wait
                robotData,robotWayPoints,action = computeRobotStep(robotData,robotWayPoints,moveDistance)
                if action != None:
                    action = action.lower()
                    if 'litter' in action:
                        littersDF.loc[action,tPlus1] = False
                        robotData['litterCount'] += 1
                        robotsWaitingTime[robot] = litProcessingTime # process picked litter
                    elif 'reuse' in action or 'end' in action:
                        nestDF.loc[tPlus1,'litterCount'] = nestDF.loc[tPlus1,'litterCount'] + robotData['litterCount']
                        nestDF.loc[tPlus1,'tPlusProcessing'] = nestDF.loc[tPlus1,'tPlusProcessing']
                        
                        robotData['litterCount'] = 0
                robotsDF.loc[tPlus1,robot] = robotData.values
    #            print(robotData)
    #            print(robotsDF.loc[str(t+timeStep),robot])
                
            else:
                robotsDF.loc[tPlus1,robot] = robotData.values
                robotsWaitingTime[robot] -= timeStep
            if robotsWaitingTime[robot] < 0:
                robotsWaitingTime[robot] = 0
                
            if len(robotWayPoints) == 0:
                numRobotsFinishedWayPoints += 1
        if numRobotsFinishedWayPoints == len(foragingWayPointsDF.keys()):
            print('Task completed')
            break
    #        if action != None:
                
        #increase time 
        t = round(t + timeStep,1)
        
        print(t)
    ani = animateForaging.animateForaging(robotsDF,littersDF,nestDF,foragingWayPointsDF.keys())
    vidname = wayPointsFile.replace('.xy','-litProcessing-') + str(litProcessingTime) + 's.mp4'
    ani.save('plots/' + vidname)
    
    fig,ax = plt.subplots()
    nestDF.plot(x='tPlusProcessing',y='litterCount',ax=ax)
    ax.set_ylim([0,210])
    ax.set_xlim([0,nestDF['tPlusProcessing'].iloc[-1] * 1.05])
    ax.legend().remove()
    ax.set_ylabel('Litter in Nest')
    ax.set_xlabel('Time in seconds')
    fig.savefig('plots/' + vidname[:-4] + '.pdf',bbox_inches='tight')
    plt.close()
    nestDF.to_csv('plots/' + vidname[:-4] + '.csv')

def loopThroughDataFiles():
    timeStep = 1 # second
    robotVelocity = 0.605 #metres/seconds
    for initialWorldStateFile in glob('CSVresults/*.csv'):
        initialWorldStateFile = ntpath.basename(initialWorldStateFile)
        for wayPointsFile in glob('results/' + initialWorldStateFile[:-4] + '*'):
            wayPointsFile = ntpath.basename(wayPointsFile)
            for litProcessingTime in [0,5]:
                simulateForagingAndSaveResults(initialWorldStateFile,wayPointsFile,timeStep,litProcessingTime,robotVelocity)
#   
if __name__ == '__main__':
    loopThroughDataFiles()