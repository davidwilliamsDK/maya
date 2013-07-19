'''
import dsCore.maya.dsCamera as dsCam
reload(dsCam)
'''
"""
If there is any curves, generate the syntax for an animation
#{curve x1 -17.12056093 x20 -17.12056093 x40 -17.12056093} {curve x1 21.66167238 x20 21.66167238 x40 54.66167238}
{curve xkeyframe value, }
"""
"""
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
"""
'''
horizontalFilmAperture
verticalFilmAperture
['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'cr', 'cg', 'cb', 'intensity', 'rotateOrder']
focalLength
['hfa', 'vfa', 'fl', 'lsr', 'fs', 'fd', 'sa', 'coi']
['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
attributes = ['', ]'''

'''
camera1.rotateX
camera1.rotateY
camera1.rotateZ
camera1.scaleX
camera1.scaleY
camera1.scaleZ
camera1.translateX
camera1.translateY
camera1.translateZ
cameraShape1.centerOfInterest
cameraShape1.fStop
cameraShape1.focalLength
cameraShape1.focusDistance
cameraShape1.horizontalFilmAperture
cameraShape1.lensSqueezeRatio
cameraShape1.shutterAngle
cameraShape1.verticalFilmAperture

'''
import pymel.core as pm
import maya.cmds as cmds
import sys, os, re

def export():
    if sys.platform == "linux2":
        home = os.getenv("HOME")
    elif sys.platform == 'win32':
        home = 'C:%s' % os.getenv("HOMEPATH")
    outputPath = '%s/camera.nk' % (home)
    formatCamera(getAllSelectedAnimAttrDict())

def formatCamera(li):
    for d in li:
        print d
        for key, value in d.items():
            '''
            minor fix for cameras only...
            '''
            print key, item
            '''name, attr = key.split('.')
            camObj = pm.ls(name, type='camera')
            if pm.nodeType(camObj) == 'camera':
                print name, attr, d[key]
            '''
    
def getAllSelectedAnimAttrDict():
    li =[]
    for shape in pm.ls(sl=True):
        animDict = getAttributeDict(shape)
        for key, value in animDict.items():
            li.append( animatedAttribute(key, value))
    return li
    
def getAttributeDict(shape):
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
    return [src for src in transform.sources() if  'animCurve' in pm.nodeType(src)]

def animatedAttribute(name, attrDict):
    '''
    Attribute is a vector3
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
    animCurveDict = {}
    for index in range(curve.numKeys()):
        animCurveDict[int(curve.getTime(index))] = curve.getValue(index)
    return animCurveDict


