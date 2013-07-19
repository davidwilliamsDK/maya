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
light1.['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'cr', 'cg', 'cb', 'intensity', 'rotateOrder']

'''
try:
    import pymel.core as pm
    import maya.cmds as cmds
except:
    pass
import sys, os, re

class mObject(object):
    def __init__(self, **kwargs):
        self.setup(kwargs)
        
    def setup(self, d):
        for k, v in d.items():
            setattr(self, k, v)
def export():
    '''
    Export a nuke file out with all the selected object from maya. 
    '''

def toNukeFormat():
    '''
    Formats to a string which can be writen to nuke.
    '''
    
def getBlah(obj, attr):
    '''
    check if obj.attr is animated else just do toNukeFormat
    if its animated get the animCurve and do animatedAttribute and then toNukeFormat
    '''
def getAllSelectedAnimAttrDict():
    li =[]
    for shape in pm.ls(sl=True):
        animDict = getAttributeDict(shape)
        for key, value in animDict.items():
            li.append( animatedAttribute(key, value))
    return li
    
def getAttributeDict(shape):
    '''return a dictionary[shape, attribute] = (dictionary[time] = value)'''
    attrDict = {}
    for animCurve in getAnimCurve(shape):
        attrName = animCurve.outputs(plugs=True)[0]
        if animCurve: attrDict[(shape, attrName)] = getAnimDict(animCurve)
    return attrDict
    
def getAnimCurve(node):
    '''
    If node or nodes parent is a transform node.
        returns a AnimCurve node.
    '''
    
    type = pm.nodeType(node)
    if type == 'transform':
        return getAnimCurveFromTransform(node)
    else:
        parent = node.getParent()
        if pm.nodeType(parent) == 'transform':
            return getAnimCurveFromTransform(parent)
        else:
            print node, 'is none of the requered nodeTypes...'
            return None
        
def getAnimCurveFromTransform(transform):
    '''Check the source of the transform if animCurve is in the nodeType'''
    return [src for src in transform.sources() if  'animCurve' in pm.nodeType(src)]

def animatedAttribute(name, attrDict):
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
    d[name] = string
    return d

def getAnimDict(curve):
    '''Takes a animCurve and from the number of keys it returns a dictionary[time] = value'''
    animCurveDict = {}
    for index in range(curve.numKeys()):
        animCurveDict[int(curve.getTime(index))] = curve.getValue(index)
    return animCurveDict


if __name__ == "__main__":
    '''For testing purpos only'''
    new = mObject(name='blah', transform=['blah'])
    print new.name, new.transform