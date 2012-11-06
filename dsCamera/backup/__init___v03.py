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
except:
    pass
import sys, os, re, math

class mObject(object):
    def __init__(self, node, **kwargs):
        self.setup(kwargs)
        self.transform = node
        self.shape = self.transform.getShape()
        self.type = pm.nodeType(self.shape)
        
        self.setAttributes()
        
    def setAttributes(self):
        attrType = self.type.lower() 

        if attrType == 'camera':
            for t in [ 'centerOfInterest', 'fStop', 'focalLength', 'focusDistance', 'horizontalFilmAperture', 'lensSqueezeRatio', 'shutterAngle', 'verticalFilmAperture']:
                #print self.checkAttribute(self.transform.attr(t))
                setattr(self, t, self.checkAttribute(self.transform.attr(t)))
        elif attrType == 'mesh':
            pass
        elif attrType == 'pointlight':
            pass
        elif attrType == 'directionallight':
            pass
        elif attrType == 'spotlight':
            pass
        elif attrType == 'locator':
            pass
        else:
            print '%', attrType
        '''
        Check if there is any animation, 
        if there is return animation in nuke format back
        else return the value in nuke format
        ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
        vector3s needs to go together
        '''
        for t in ['translate', 'rotate', 'scale', 'v', 'rotateOrder']:
            #print  self.checkAttribute(self.transform.attr(t))
            attributes = self.checkAttribute(self.transform.attr(t))
            print attributes
            try:
                setattr(self, t, attributes)
            except Exception as e:
                print e
                
    
    def checkAttribute(self, attr):
        '''Check if there is any animation on the given attribute'''
        '''translate {{curve x1 0 x30 1} {curve x1 1.323 x12 2 x30 1.2} {curve x1 0 x20 1 x30 0.3}}'''
        
        name = attr.longName()
        if name in ['translate', 'rotate', 'scale']:
            string = '%s {' % (name)
            for axis in ['X','Y','Z']:
                axisAttr = self.transform.attr('%s%s'% (name, axis))
                if axisAttr.connections():
                    for curve in axisAttr.connections():
                        if  'animCurve' in pm.nodeType(curve):
                            string +=  '{curve%s} ' % (self.getAnimDict(curve))
                else:
                    string += '%04.2f ' % (axisAttr.get())
            return '%s}' % (string.strip())
        else:
            connections = attr.connections()
            print connections
            if connections:
                return self.toNukeFormat(attr)
            else:
                return '%s %04.2f' % (name, attr.get())       


    def getAnimDict(self, curve):
        '''Takes a animCurve and from the number of keys it returns a dictionary[time] = value'''
        animCurveDict = {}
        for i in range(curve.numKeys()):
            animCurveDict[int(curve.getTime(i))] = '%04.2f' % (pm.keyframe(curve, index=i, query=True, eval=True))[0]
            #animCurveDict[int(curve.getTime(index))] = '%04.2f' % (curve.getValue(index))
        return self.animAttributeToNuke(animCurveDict)
    
    def animAttributeToNuke(self, attrDict):
        '''
        Attribute is a vector3
        converts attrDict in to a dictionary[attribute] =  xtime value
        '''
        
        string = ''
        d ={}
        sortedKeys = attrDict.keys()
        sortedKeys.sort()
        for key in sortedKeys:
            string += ' x%s %s' % (key, attrDict[key])
        return string
        
    def toNukeFormat(self, attr):
        '''
        Formats to a string which can be writen to nuke.
        '''
        d ={}
        name = attr.longName()
        string = '%s {' % (name)
        for curve in attr.connections():
            if  'animCurve' in pm.nodeType(curve):
                string +=  '{curve%s} ' % (self.getAnimDict(curve))
        string = '%s}\n' % (string.strip())
        d[name] = string
        return d
                    
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
        print '[%s]%s' % (pm.nodeType(node) , node)
        if pm.nodeType(node) == 'transform':
            obj = mObject(node)
            objList.append(obj)
    writeNukeFile(objList)
            
def toNuke(objList):
    string = ''
    for obj in objList:
        if obj.type == 'camera':
            string += 'Camera2 {\n'
            for attr in ['translate','rotate', 'scale', 'rotateOrder']:
                string += '%s\n' % (getattr(obj, attr))
            string += '}\n'
        if obj.type == 'locator':
            string += 'Axis2 {\n'
            for attr in ['translate','rotate','scale', 'rotateOrder']:
                string += '%s\n' % (getattr(obj, attr))
            string += '}\n'
    return string

def writeNukeFile(objList):
    if sys.platform == "linux2":
        home = os.getenv("HOME")
        outputPath = '%s/camera.nk' % (home)
    elif sys.platform == 'win32':
        home = 'C:%s' % os.getenv("HOMEPATH")
        outputPath = '%s\camera.nk' % (home)
    
    print outputPath
    file = open(outputPath, 'w')
    file.write( toNuke(objList))
    file.close()
    


if __name__ == "__main__":
    '''For testing purpos only'''
    new = mObject(name='blah', transform=['blah'])
    print new.name, new.transform