try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass
import sys, os, re, math
import dsCommon.dsMayaEnv as dsENV

class mObject(object):
    def __init__(self, node):
        self.transform = node
        self.name = self.transform.shortName()
        self.shape = self.transform.getShape()
        self.type = pm.nodeType(self.shape)
        self.attributes = []
        self.setAttributes()

    def setAttributes(self):
        '''Maya attributes only...'''
        
        attrType = self.type.lower() 

        if attrType == 'camera':
            for attr in [ 'centerOfInterest', 'fStop', 'focalLength', 'focusDistance', 'horizontalFilmAperture', 'lensSqueezeRatio', 'shutterAngle', 'verticalFilmAperture', 'nearClipPlane', 'farClipPlane']:
                self.setAttr(attr)
        
        elif attrType in ['pointlight', 'directionallight', 'spotlight']:
            self.attributes.append('light_type')
            
            if attrType == 'pointlight':
                setattr(self, 'light_type', dict({'light_type':'point'}))
                
            if attrType == 'directionallight':
                setattr(self, 'light_type', dict({'light_type':'directional'}))
                
            if attrType == 'spotlight':
                setattr(self, 'light_type', dict({'light_type':'spot'}))
                
            for attr in ['intensity', 'color']:
                self.setAttr(attr)
        
        elif attrType == 'mesh':
            pm.select(self.transform)
            self.attributes.append('file')
            setattr(self, 'file', dict({'file':pm.exportSelected('%s/%s' %( os.getenv("HOME"), self.transform.shortName()), constraints=False, force=True, type='FBX export')}))
        
        elif attrType == 'locator':
            pass
        
        else:
            print '%', attrType

        for attr in ['translate', 'rotate', 'scale', 'rotateOrder']:
            self.setAttr(attr)

    def setAttr(self, attr):
        self.attributes.append(attr)
        setattr(self, attr, self.checkAttribute(self.transform.attr(attr)))
        
    def checkAttribute(self, attr):
        d={}
        name = attr.longName()
        print attr.type()
        if attr.type() == 'double3' or attr.type() == 'float3':
            string = '{'
            for childAttr in attr.children():
                if childAttr.isConnected():
                    string += '{curve%s} ' % (self.getAnimDict(childAttr))
                else:
                    string += '%04.2f ' % (childAttr.get())
            d[name] = '%s}' % (string.strip())
            return d
        else:
            d[attr.longName()] = attr.get()
            return d
            
    def getAnimDict(self, attr, multiply=None):
        '''Takes a animCurve and from the number of keys it returns a dictionary[time] = value'''
        d = {}
        for i in pm.keyframe(attr, query=True):#range(len(
            d[int(i)] = '%04.2f' % pm.keyframe(attr, time=(int(i), int(i)), query=True, eval=True)[0]
                
        return self.animAttributeToNuke(d)
    
    def animAttributeToNuke(self, attrDict):
        '''
        Attribute is a vector3
        converts attrDict in to a dictionary[attribute] =  xtime value
        '''
        string = ''
        d={}
        sortedKeys = attrDict.keys()
        sortedKeys.sort()
        for key in sortedKeys:
            string += ' x%s %s' % (key, attrDict[key])
        return string
    
def export():#path
    outPath = setEnv()
    outPath = outPath + "/camExport"
    objList = []
    for node in pm.ls(sl=True):
        if pm.nodeType(node) == 'transform':
            obj = mObject(node)
            objList.append(obj)
            if obj.type == 'mesh':
                try:
                    mel.eval('deleteUI FbxWarningWindow;')
                except Exception as e:
                    print 'Error:%s' % e
    writeNukeFile(objList,outPath)

def exportCamSeq():#path
    outPath = setEnv()
    shotList = []
    for shot in cmds.ls(type="shot"):
        if re.search("s[0-9][0-9][0-9][0-9]",shot):
            shotList.append(shot)

    for shot in shotList:
        newoutPath = outPath + "/" + shot + "/comp/3DExport/camExport"
        camera = cmds.shot(shot, q=True,cc=True)
        objList = []
        node = cmds.select(camera)
        cam = cmds.listRelatives( camera, p=True )
        camNode = cam[0]
        cmds.select(camNode)
        for node in pm.ls(sl=True):
            if pm.nodeType(node) == 'transform':
                obj = mObject(node)
                objList.append(obj)
                if obj.type == 'mesh':
                    try:
                        mel.eval('deleteUI FbxWarningWindow;')
                    except Exception as e:
                        print 'Error:%s' % e
        writeNukeFile(objList,newoutPath)

def toNuke(objList):
    string = ''
    for obj in objList:
        
        if obj.type == 'camera':
            string += nukeNode(obj, 'Camera2')
            
        if obj.type == 'locator':
            string += nukeNode(obj, 'Axis2')
            
        if obj.type == 'mesh':
            string += nukeNode(obj, 'ReadGeo2')
            
        if obj.type in ['pointLight', 'directionalLight', 'spotLight']:
            string += nukeNode(obj, 'Light2')
            
    string += 'Scene {\n inputs %s\n}\n' %(len(objList))
    return string

def nukeNode(obj, nodeName, ):
    string = '%s {\n' % (nodeName)
    string += 'inputs 0\n'
    string += 'name %s\n' %(obj.name)
    
    for attr in obj.attributes:
        #print 'nukeNode', nodeName, attr
        try:
            d = getattr(obj, attr)
        except Exception as e:
            print 'eerrrooor', e
        
        nukeName = getNukeAttributeName(attr)
        if nukeName:
            if 'aperture' in nukeName:
                string += '%s %s\n' % (nukeName, (d[attr] * float(25.4)))
            else:
                #print 'here', attr, type(d)
                string += '%s %s\n' % (nukeName, d[attr])
    string += '}\n'
    return string

def getNukeAttributeName(string):
    if string.lower() == 'rotateorder':
        return 'rot_order'
    
    elif string.lower() == 'scale':
        return 'scaling'
    
    elif string == 'horizontalFilmAperture':
        return 'haperture'
    
    elif string == 'verticalFilmAperture':
        return 'vaperture'
    
    elif string== 'focalLength':
        return 'focal'
    
    elif string == 'focusDistance':
        return 'focal_point'
    
    elif string == 'nearClipPlane':
        return 'near'
    
    elif string == 'farClipPlane':
        return 'far'
    
    elif string == 'fStop':
        pass

    elif string == 'centerOfInterest':
        pass
    
    elif string == 'lensSqueezeRatio':
        pass
    
    elif string == 'shutterAngle':
        pass
    else:
        return string

def setEnv():
    dsENV.setGlobals()
    project = '%s' % os.getenv('PROJECT')
    episode = '%s' % os.getenv('EPISODE')
    sequence = '%s' % os.getenv('SEQUENCE')
    print '%s/%s/film/%s/%s' % ("/dsComp", project, episode, sequence)
    if sys.platform == "linux2":
        outPath = '%s/%s/film/%s/%s' % ("/dsComp", project, episode, sequence)
    elif sys.platform == "win32":
        outPath = '%s/%s/film/%s/%s' % ("S:/", project, episode, sequence)
    return outPath

def writeNukeFile(objList,outPath):
    if not os.path.isdir(outPath):os.makedirs(outPath)
    
    outputPath = '%s/camera.nk' % (outPath)
    
    print 'Exporting to:', outputPath
    file = open(outputPath, 'w')
    file.write( toNuke(objList))
    file.close()
    
def checkCameraName():
    camList = cmds.ls(cameras=True)
    for cam in camList:
        camName = cmds.listRelatives(cam,allParents=True)
        if camName[0] != "front" or camName[0] != "persp" or camName[0] != "side" or camName[0] != "top":
            print camName[0]
            if not re.search("s[0-9][0-9][0-9][0-9]",camName[0]):
                print "run the camera clean up script please"
                
            else:
                print "match"
                exportCamSeq()
                break