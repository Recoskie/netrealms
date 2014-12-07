import copy
import math
import engine
import pygame
import time

#******************map width and height number of tiles search***********************

MWidth=1024
MHeight=768

#*******************************visited squares**************************************

VisitedList=[]

#*****************************debug mode setting*************************************

DebugMode=False

#**************************turn Debug mode off or on*********************************

def setDebugMode(YesNo ):
    global DebugMode
    DebugMode = YesNo

#**********************check if debug setting is off or on***************************

def isDebugOn():
    return(DebugMode )

#*************show visited squares helps to debug algorithm problems****************

def displyVisitedPoints(screen ):
    for i in VisitedList:
        pygame.draw.rect(screen,(0,255,255), (i[0],i[1],32,32), 1)
    pygame.display.update()
            
#********Improves performance Estimate Closest Path rearrange the path list**********
#************************to scan the shortest path first*****************************

def estimateBestPath(x2, y2, paths ):
    PathElement=0
    CurrentDif=0
    OldDif=0

    PathElement=0
    OldDif=math.sqrt((math.pow((x2-paths[0][len(paths[0])-1][0]),2)+math.pow((y2-paths[0][len(paths[0])-1][1]),2)))

    for i in range(1,len(paths)):
        CurrentDif=math.sqrt((math.pow((x2-paths[i][len(paths[i])-1][0]),2)+math.pow((y2-paths[i][len(paths[i])-1][1]),2)))

        if(CurrentDif<OldDif):
                PathElement=i
                OldDif=CurrentDif

    if(not PathElement==0):
        c=copy.copy(paths[0])
        paths[0]=paths[PathElement]
        paths[PathElement]=c

    return(paths )

#********************check if Point has not been Visited****************************

def notVisited(x1, y1 ):

    global VisitedList
    
    for i1 in reversed(VisitedList):
        if(i1[0]==x1 and i1[1]==y1):
            return(False)
    return(True)

#********************************get each move**************************************

def getMoves(x1, y1, BlkTiles ):
    
    global VisitedList
    MoveList=[]

    YMove=32
    XMove=32
    
    if(not y1<=0):
        if(not engine.isBlockTiles(x1,(y1-YMove),BlkTiles) and notVisited(x1,(y1-YMove))):
            VisitedList.append([x1,(y1-YMove)])
            MoveList.append([x1,(y1-YMove)])

    if((y1+YMove)<MHeight):
        if(not engine.isBlockTiles(x1,(y1+YMove),BlkTiles ) and notVisited(x1,(y1+YMove))):
            VisitedList.append([x1,(y1+YMove)])
            MoveList.append([x1,(y1+YMove)])

    if(not x1<=0):
        if(not engine.isBlockTiles((x1-XMove),y1,BlkTiles) and notVisited((x1-XMove),y1)):
            VisitedList.append([(x1-XMove),y1])
            MoveList.append([(x1-XMove),y1])

    if((x1+XMove)<MWidth):
        if(not engine.isBlockTiles((x1+XMove),y1,BlkTiles) and notVisited((x1+XMove), y1 )):
            VisitedList.append([(x1+XMove),y1])
            MoveList.append([(x1+XMove),y1])

    #return the moves that can be made from current path

    return(MoveList)

#*************************path finding algorithm start*****************************

def findPath(screen, x1, y1, x2, y2, BlkTiles ):

    IsPaths=True

    x1=int(x1/32+0.5)*32
    y1=int(y1/32+0.5)*32
    x2=int(x2/32+0.5)*32
    y2=int(y2/32+0.5)*32

    global VisitedList
    VisitedList=[[x1, y1 ]]
    PathList=[ [ [x1, y1 ] ] ]

    #check if start is block tile

    if(engine.isBlockTiles(x1+32, y1+48, BlkTiles )):
       return(PathList[0])

    #check if end is block tile
    
    if(engine.isBlockTiles(x2+32, y2+48, BlkTiles )):
       return(PathList[0])

    while PathList:
        
        x=PathList[0][len(PathList[0])-1][0]
        y=PathList[0][len(PathList[0])-1][1]

        #if path reached goal return path points to goal
        if ((x>=x2 and x<=(x2+32)) and (y>=y2 and y<=(y2+32))):
                        return(PathList[0])
        
        m=getMoves(x, y, BlkTiles )
        
        for i in m:
            c=copy.copy(PathList[0])
            c.append(i)
            c=copy.copy(c)
            PathList.append(c)
        PathList.pop(0)

        #graphically display current Visited squares by other paths if debug mode enabled

        if DebugMode:
            displyVisitedPoints(screen )
            time.sleep(0.02)
        
        #rearrange paths for performance
        if PathList:
            PathList=estimateBestPath(x2, y2, PathList )

    #if no path to destination send back start point
    return([[x1,y1]])
