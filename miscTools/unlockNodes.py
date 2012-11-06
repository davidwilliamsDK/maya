from maya.cmds import *
def unlockNodes():
    
    nodes = ls(sl=True, long=True)
    for node in nodes:
        lockNode(node, l=False)
        children = listRelatives(node, children=True, allDescendents=True, fullPath=True)
        for child in children:
            lockNode(child, l=False)
unlockNodes()