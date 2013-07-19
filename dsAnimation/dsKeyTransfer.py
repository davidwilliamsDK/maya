import maya.cmds as cmds

obj = cmds.ls(selection=True)

def getCtrlWKeys(obj):
    objSplit = obj.split(":")
    ns = objSplit[0]
    ctrlList = []
    dag = cmds.ls( ns + ':*',dagObjects=True,r=True)
    cmds.select(cl=True)    
    
    for d in dag:
        objKeys = cmds.keyframe( d, query=True, valueChange=True, timeChange=True)
        if objKeys != None:
            ctrlList.append(d)
            print d
            print objKeys
            
    cmds.select(ctrlList)
           

def readAnimExport(ns):
    tmpFile = "/home/admin/maya/projects/default/scenes/test.anim"
    
    f = open(tmpFile, "r")
    searchlines = f.readlines()
    f.close()
    
    transferSelList = []
    for i, line in enumerate(searchlines):
        if re.search(ns,line):
            tmpLine = line
            tmpSplit = tmpLine.split(" ")
            for tmp in tmpSplit:
                if re.search(ns,tmp):
                    if tmp not in transferSelList:
                        transferSelList.append(tmp)
    
    print transferSelList
    
def applyAnimExport(ns,tns,transferSelList):
    newTransferList = []
    for tsl in transferSelList:
        newCtrl = tsl.replace(ns,tns)
        newTransferList.append(newCtrl)
    return newTransferList


if len(obj) == 2:
    objSplit = obj[1].split(":")
    tns = objSplit[0]
    print "NEW NAMESPACE ===== " + tns
    
if len(obj) == 1:
    tns = ns

#getCtrlWKeys(obj[0])
readAnimExport(ns)
transferSelList = applyAnimExport(ns,tns,transferSelList)

cmds.select(transferSelList)




import maya.cmds as cmds

obj = cmds.ls(selection=True)

def getCtrlWKeys(obj):
    objSplit = obj.split(":")
    ns = objSplit[0]
    ctrlList = []
    dag = cmds.ls( ns + ':*',dagObjects=True,s=False,r=True)
    cmds.select(cl=True)    
    cmds.select(dag)
    
    #for d in dag:
        #print d
        #objKeys = cmds.keyframe( d, query=True, valueChange=True, timeChange=True)
        #if objKeys != None:
            #ctrlList.append(d)
            #print d
            #print objKeys
            
    #cmds.select(ctrlList)
          
          
getCtrlWKeys(obj[0])