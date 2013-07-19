import maya.cmds as cmds
import re, os

def GetFrame():
##    print cmds.currentTime(query=True)
    return cmds.currentTime( query=True )

def GetSeqName():
    dsSeq = str(os.getenv('SEQUENCE'))
    return str(dsSeq)

def GetShotName():
    dsShot = str(os.getenv('SHOT'))
    return str(dsShot)

def GetShotDuration():
    dsShot = str(os.getenv('SHOT'))
    ShotDuration = cmds.shot(str(dsShot), q=True, sd=True)
    return ShotDuration

def GetShotFrame():
    dsShot = str(os.getenv('SHOT'))
    ShotStart = cmds.shot(str(dsShot), q=True, st=True)
    currentTime = cmds.currentTime(query=True)
    return currentTime - ShotStart + 1