'''
import dsCore.maya.dsCamera as dsCam
reload(dsCam)

{curve x1 -17.12056093 x20 -17.12056093 x40 -17.12056093} {curve x1 21.66167238 x20 21.66167238 x40 54.66167238}

%NAME% {
 translate {%Tx% %Ty% %Tz%}
 rotate {%Rx% %Ry% %Rz%}
 uniform_scale 2
 pivot {0 1 0}
 focal %FOCAL%
 haperture %HAPERTUR%
 vaperture %VAPERTUR%
 near %NEAR%
 far %FAR%
 focal_point %FOCALPOINT%
 fstop %FSTOP%
 name %NAME%
}


camera1.['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
cameraShape1.['hfa', 'vfa', 'fl', 'lsr', 'fs', 'fd', 'sa', 'coi']
cameraShape1.centerOfInterest
cameraShape1.fStop
cameraShape1.focalLength
cameraShape1.focusDistance
cameraShape1.horizontalFilmAperture * 25.4
cameraShape1.lensSqueezeRatio
cameraShape1.shutterAngle
cameraShape1.verticalFilmAperture * 25.4
camera1.rotateX
camera1.rotateY
camera1.rotateZ
camera1.scaleX
camera1.scaleY
camera1.scaleZ
camera1.translateX
camera1.translateY
camera1.translateZ
light1.['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'cr', 'cg', 'cb', 'intensity', 'rotateOrder']

        if ($mayaRotOrder == 0) {
            $rotOrder = "XYZ";
            }
        if ($mayaRotOrder == 1) {
            $rotOrder = "YZX";
            }
        if ($mayaRotOrder == 2) {
            $rotOrder = "ZXY";
            }
        if ($mayaRotOrder == 3) {
            $rotOrder = "XZY";
            }
        if ($mayaRotOrder == 4) {
            $rotOrder = "YXZ";
            }
        if ($mayaRotOrder == 5) {
            $rotOrder = "ZYX";
            }
'''
try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass
import sys, os, re, math

class mObject(object):
    def __init__(self, node, **kwargs):
        self.attributeList=[]
        self.setup(kwargs)
        self.transform = node
        self.name = self.transform.shortName()
        self.shape = self.transform.getShape()
        self.type = pm.nodeType(self.shape)
        self.setAttributes()
        
    def getAttributeList(self):
        return self.attributeList
    
    def setAttributes(self):
        attrType = self.type

        if attrType == 'camera':
            for t in [ 'centerOfInterest', 'fStop', 'focalLength', 'focusDistance', 'horizontalFilmAperture', 'lensSqueezeRatio', 'shutterAngle', 'verticalFilmAperture']:
                self.attributeList.append(t)
                setattr(self, t, self.checkAttribute(self.transform.attr(t)))
                
        elif attrType == 'mesh':
            for t in ['file']:
                self.attributeList.append(t)
                #print 'Exporting', self.transform
                pm.select(self.transform)
                setattr(self, t, dict({t:pm.exportSelected('%s/%s' %( os.getenv("HOME"), self.transform.shortName()), constraints=False, force=True, type='FBX export')}))
                
        elif attrType in ['pointLight', 'directionalLight', 'spotLight']:
            #Light2
            for t in [ 'intensity', 'color' ]:
               self.attributes.append(t)
               setattr(self, t, self.checkAttribute(self.transform.attr(t)))
        else:
            print '%s', attrType
            
        '''
        Check if there is any animation, 
        if there is return animation in nuke format back
        else return the value in nuke format
        ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
        vector3s needs to go together
        '''
            
        for t in ['translate', 'rotate', 'scale', 'rotateOrder']:
            #print self.transform.attr(t)
            self.attributeList.append(t)
            attributes = self.checkAttribute(self.transform.attr(t))
            #print attributes
            try:
                setattr(self, t, attributes)
            except Exception as e:
                print e

    def checkAttribute(self, attr):
        '''
        Check if there is any animation on the given attribute
        translate {{curve x1 0 x30 1} {curve x1 1.323 x12 2 x30 1.2} {curve x1 0 x20 1 x30 0.3}}
        '''
        d={}
        name = attr.longName()
        #: If vector3
        if attr.type() == 'double3':
            string = '{'
            for axis in ['X','Y','Z']:

                axisAttr = self.transform.attr('%s%s'% (name, axis))
                if axisAttr.connections():
                    for curve in axisAttr.connections():
                        if  'animCurve' in pm.nodeType(curve):
                            string += '{curve%s} ' % (self.getAnimDict(curve))
                else:
                    string += '%04.2f ' % (axisAttr.get())
            string = '%s}' % (string.strip())
            d[name] = string
            return d
        else:

            connections = attr.connections()

            if attr.isConnected():
                if attr.type() == 'enum':
                    d[name] = '%s' % (attr.get(asString=True))  
                else:
                    d[name] = self.toNukeFormat(attr)
                return d
            else:
                
                if 'FilmAperture' in name:
                    d[name] = '%04.2f' % (float(attr.get()) * 25.4)
                else:
                    value = attr.get()
                    if type(value) is float or type(value) is int:
                        d[name] = '%04.2f' % (attr.get())
                    else:
                        print name, type(value)
                return d

    def getAnimDict(self, curve, multiply=None):
        '''Takes a animCurve and from the number of keys it returns a dictionary[time] = value'''
        animCurveDict = {}
        for i in range(curve.numKeys()):
            if multiply:
                animCurveDict[int(curve.getTime(i))] = '%04.2f' % (float(pm.keyframe(curve, index=i, query=True, eval=True)[0]) * float(multiply))
            else:
                animCurveDict[int(curve.getTime(i))] = '%04.2f' % (pm.keyframe(curve, index=i, query=True, eval=True))[0]
        return self.animAttributeToNuke(animCurveDict)

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
        
    def toNukeFormat(self, attr):
        '''
        Formats to a string which can be writen to nuke.
        '''
        name = attr.longName()
        string = '{'
        for curve in attr.connections():
            if 'animCurve' in pm.nodeType(curve):
                if 'FilmAperture' in name:
                    string +=  '{curve%s} ' % (self.getAnimDict(curve, 25.4))
                else:
                    string +=  '{curve%s} ' % (self.getAnimDict(curve))
        string = '%s}\n' % (string.strip())
        return string
                    
    def setup(self, d):
        for k, v in d.items():
            setattr(self, k, v)

        
def export():
    '''
    Export a nuke file out with all the selected object from maya. 
    Takes care of all exporting
    need: shape and transform
    because might need some attributes from them
    '''
    objList = []
    for node in pm.ls(sl=True):
        #print '[%s]%s' % (pm.nodeType(node) , node)
        if pm.nodeType(node) == 'transform':
            obj = mObject(node)
            objList.append(obj)
    writeNukeFile(objList)
    mel.eval('deleteUI FbxWarningWindow;')
            
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

def nukeNode(obj, nodeName):
    string = '%s {\n' % (nodeName)
    string += 'inputs 0\n'
    string += 'name %s\n' %(obj.name)
    
    for attr in obj.getAttributeList():
        try:
            d = getattr(obj, attr)
        except Exception as e:
            print 'eerrrooor', e

        nukeName = getNukeAttributeName(attr)
        string += '%s %s\n' % (nukeName, d[attr])
    string += '}\n'
    return string

def getNukeAttributeName(string):
    #what the fuck is win_scales
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
    
    elif string == 'fStop':
        return 'scaling'
    
    elif string == 'centerOfInterest':
        return 'scaling'
    
    elif string == 'lensSqueezeRatio':
        return 'scaling'
    
    elif string == 'shutterAngle':
        return 'scaling'
    else:
        return string
    
def writeNukeFile(objList):
    if sys.platform == "linux2":
        home = os.getenv("HOME")
        outputPath = '%s/camera.nk' % (home)
    elif sys.platform == 'win32':
        home = 'C:%s' % os.getenv("HOMEPATH")
        outputPath = '%s\camera.nk' % (home)
    
    print 'Exporting to:', outputPath
    file = open(outputPath, 'w')
    file.write( toNuke(objList))
    file.close()
    


if __name__ == "__main__":
    '''For testing purpos only'''
    new = mObject(name='blah', transform=['blah'])
    #print new.name, new.transform