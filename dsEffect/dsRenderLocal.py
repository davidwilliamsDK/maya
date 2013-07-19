
import maya.cmds as cmds
import maya.mel as mel

def dsRenderLocal(start,end):
    y = start
    x = end
    while y <= x:
        cmds.currentTime(y)
        mel.eval('renderWindowRender redoPreviousRender renderView;')
        y = y + 1
        
#sRenderLocal(140,150)