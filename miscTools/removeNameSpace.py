from maya.cmds import *
def removeNamespace(topNode):
    if ':' in topNode:
        newNode = topNode.split(':')[-1]
        rename(topNode, newNode)
        topNode = newNode
        
    children = listRelatives(topNode, children=True, fullPath=True)
    if children:
        for child in children:
            if ':' in child:
                lastName = child.split('|')[-1]
                newChild = child.split(lastName)[0] + child.split(':')[-1]
                rename(child, child.split(':')[-1])
                child = newChild
                
            removeNamespace(child)
nodes = ls(sl=True)
for node in nodes:
    removeNamespace(node)


