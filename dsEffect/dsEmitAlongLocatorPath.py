import maya.cmds as cmds
import math

def dsEmitAlongLocator(start,end,ss):
    y = start
    x = end
    cmds.currentTime(y)
    
    locX = cmds.getAttr('locator1.translateX')
    locY = cmds.getAttr('locator1.translateY')
    locZ = cmds.getAttr('locator1.translateZ')
    beforePos = [locX,locY,locZ]
    
    while y <= x:
        cmds.currentTime(y)
        locX = cmds.getAttr('locator1.translateX')
        locY = cmds.getAttr('locator1.translateY')
        locZ = cmds.getAttr('locator1.translateZ')
        pos = [locX,locY,locZ]
        
        dist = [pos[0]-beforePos[0],pos[1]-beforePos[1],pos[2]-beforePos[2]]
        val = [dist[0]/ss,dist[1]/ss,dist[2]/ss]

        for i in range(ss):
            beforePos = [beforePos[0]+val[0],beforePos[1]+val[1],beforePos[2]+val[2]]
            cmds.emit( object='trail_pt', pos=(beforePos))
            
        beforePos = pos
        y = y + 1

        
#dsEmitAlongLocator(0,25,25)
import maya.cmds as cmds
import re

def testParticle(partObj,particleId):

    try:
        cmds.particle( partObj, q=True, id=int(particleId), attribute="age" )
        return 1
    except:
        return 0
    
def readASC(ascPath,partObj):
    print ascPath
    ascFile = open(ascPath, 'r')
    tmpDict = {}
    
    for line in ascFile:
        if re.search("frame",line):
            tmpList = line.split(" ")
            frame = tmpList[-1].rstrip('\n')
        if re.search("particles",line):
            tmpList = line.split(" ")
            particles=tmpList[-1].rstrip('\n')
        lineList = line.split(" ")
        if len(lineList) == 10:
            objDict = {}
            objDict['id'] = lineList[0]
            objDict['x'] = lineList[1]
            objDict['y'] = lineList[2]
            objDict['z'] = lineList[3]
            objDict['vx'] = lineList[4]
            objDict['vy'] = lineList[5]
            objDict['vz'] = lineList[6]
            objDict['radius'] = lineList[7]
            objDict['density'] = lineList[8]
            objDict['pressure'] = lineList[9].rstrip("\r\n")
            tmpDict[lineList[0]] = objDict
    cmds.currentTime(int(frame))
    
    for key in tmpDict.values():
        particleId = key['id']
        particleX = key['x']
        particleY = key['y']
        particleZ = key['z']
        try:  
            if testParticle(partObj,int(particleId)) == 0:
               cmds.emit( object=partObj, pos=(float(particleX),float(particleY),float(particleZ)))
            else:
               cmds.particle( partObj, e=True, attribute='position', id=int(particleId), vectorValue= (float(particleX),float(particleY),float(particleZ)))
        except:
            pass
    ascFile.close()
    
partObj='nParticle1'

start = 0
end = 28
val = 0

while val <= end:
    padNum = "%05d" % val
    ascPath = "P:/Lego_Friends/film/LEGO_Friends_EP03_147768/q0360/3D/effect/rf/q0360/particles/JetSki_Engine_01_v05_"+str(padNum)+".asc"
    readASC(ascPath,partObj)
    
    val = val + 1


