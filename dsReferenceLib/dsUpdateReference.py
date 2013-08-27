import maya.cmds as cmds
import dsCommon.dsReferenceCMD as refCMD
reload(refCMD)
import os,sys,sip
from PyQt4 import QtGui, QtCore, uic
import dsCommon.dsProjectUtil as projectUtil
reload(projectUtil)

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

guiName = "dsSwapReferencesUI.ui"

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/dsReferenceLib/%s' % guiName
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsReferenceLib/%s' % guiName
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/dsReferenceLib/%s' % guiName

print 'Loading ui file:', os.path.normpath(uiFile)
form_class, base_class = uic.loadUiType(uiFile)

#Importing maya UI
try:
    import maya.OpenMayaUI as mui
except:
    pass

'''THIS IS THE MAYA WINDOW CONTROLLING THE REFERENCE SWAP'''
'''SEE FURTHER DOWN IN THIS DOC TO USE IT WITHOUT THE GUI'''
def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    ptr = long(ptr)
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class dsSwapRefTool(form_class, base_class):
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        self.updateLineEdit()
        self.presets.activated.connect(self.updateLineEdit);
        self.swap.clicked.connect(self.guiHandler)

    def guiHandler(self):
        refTag = self.custom.text()
        deleteProxies = True
        if not self.proxiesRemove.isChecked():
            deleteProxies = False
        print refTag
        output = refSwapHandler(refTag, deleteProxies)
        print output
        #self.log.setTextColor(50,500,50)
        self.log.setPlainText(str(output))

    def updateLineEdit(self):
        preset = self.presets.currentText()
        self.custom.setText(preset)

def dsUpdateRefs():
    global myWindow
    myWindow = dsSwapRefTool()
    myWindow.show()


'''GLOBAL DEFS CAN BE USED ELSE WHERE TOO'''
'''USED THE HANDLER BELOW TO SWAP ALL REFS IN A SCENE TO A DIFERENT TAG'''
def refSwapHandler(refTag=None, deleteProxies=False):
    if refTag:
        refs = currentlyLoadedRefs()
        if refs:
            print refs
            for r in refs:
                if deleteProxies:
                    refCMD.removeNonActiveProxies(r)
                updateReferences(r, refTag)
            return "Done Swapping Refs"
        else:
            return "No Valid Refs in the Scene"
    else:
        return "please provide reftag before running script"

def getAllRefs():
    files = cmds.ls(type="reference")
    refNodes = []

    for f in files:
        if not ":" in f:
            if not "sharedReferenceNode" in f:
                refNodes.append(f)

    if not refNodes == []:
        return refNodes
    else:
        return None

def updateReferences(currentRef, refTag=None):
    filetype = "mayaBinary"
    try:
        currentRefPath = cmds.referenceQuery(currentRef ,filename=True )
    except:
        currentRefPath = False
    if currentRefPath:
        if not refTag in currentRefPath:
            newReference = "%s_%s.mb" % (currentRefPath.rsplit("_",1)[0], refTag)
            if os.path.exists(newReference):
                print currentRef
                cmds.file(newReference, loadReference=currentRef, type=filetype, options="v=0")
            else:
                print "There's no Reference with that Tag for this Asset"
        else:
            print "file is already swapped"
    else:
        print "No Current file Exists for this Ref, maybe it's not loaded"

def currentlyLoadedRefs():
    refs = cmds.ls(referencedNodes=True)
    currentLoaded = []

    for ref in refs:
        try:
            path = cmds.referenceQuery(ref ,filename=True )
            refNode = cmds.referenceQuery(path, referenceNode=True)
            if not refNode in currentLoaded:
                currentLoaded.append(refNode)
        except:
            pass
    return currentLoaded

#Ex.
#refSwapHandler("Render")

##import dsReferenceLib.dsUpdateReference as updateRef
##reload(updateRef)
##
##updateRef.dsUpdateRefs()