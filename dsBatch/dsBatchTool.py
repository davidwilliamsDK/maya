import os,sys,sip
from PyQt4 import QtGui, QtCore, uic

os.environ['PATH'] = "%PATH%;C:/Program Files/Autodesk/Maya2013/bin/"
os.environ['PYTHONPATH']="%PYTHONPATH%;//vfx-data-server/dsGlobal/dsCore/maya;//vfx-data-server/dsGlobal/globalMaya/Resources/PyQt_Win64;//vfx-data-server/dsGlobal/globalResources/Shotgun;//vfx-data-server/dsGlobal/dsCore/shotgun;"
os.environ['MAYA_SCRIPT_PATH']="%MAYA_SCRIPT_PATH%;//vfx-data-server/dsGlobal/globalMaya/Mel;C:/Program Files/Autodesk/Maya2013/scripts/others;C:/Program Files/Autodesk/Maya2013/mentalray/scripts"

#Decalring Paths
guiName = "dsBatchUI.ui"
clashNameSpace = "CLASSINGELEMENT_"

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsBatch/%s' % guiName
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsBatch/%s' % guiName

print 'Loading ui file:', os.path.normpath(uiFile)
form_class, base_class = uic.loadUiType(uiFile)

#Importing maya UI
try:
    import maya.OpenMayaUI as mui
except:
    pass

def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = mui.MQtUtil.mainWindow()
    ptr = long(ptr)
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class dsVrayShapeAttr(form_class, base_class):
    def __init__(self, parent=None):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        self.python.clicked.connect(self.browsPython)
        self.add.clicked.connect(self.addMayafile)
        self.remove.clicked.connect(self.removeSelected)
        self.load.clicked.connect(self.loadFileList)
        self.run.clicked.connect(self.runBatch)
        self.save.clicked.connect(self.saveFileList)
        self.all.clicked.connect(self.selectAll)
        self.i = 0
        self.filesLoaded = []

    def browsPython(self):
        #"browsing Python Script"
        self.pyFile = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "Python Files (*.py)")
        self.script.setText(self.pyFile)

    def selectAll(self):
        for i in range(self.list.count()):
            item = self.list.item(i)
            self.list.setItemSelected(item, True)

    def addMayafile(self):
        #"adding maya file"
        self.mayaFile = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "Maya Files (*.ma *.mb)")

        if not self.mayaFile == "":
            if not self.mayaFile in self.filesLoaded:
                self.list.addItem(self.mayaFile)
                self.filesLoaded.append(self.mayaFile)

    def removeSelected(self):
        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))
            if item.text() in self.filesLoaded:
                self.filesLoaded.remove(item.text())

    def loadFileList(self):
        self.loadFile = QtGui.QFileDialog.getOpenFileName(self, "Open Text File", "", "Text File (*.txt)")
        f = open(self.loadFile, "r+")
        lines = f.readlines()

        for line in lines:
            if not line == "":
                if not line in self.filesLoaded:
                    self.list.addItem(line)
                    self.filesLoaded.append(line)
        f.close()

    def saveFileList(self):
        self.saveFile = QtGui.QFileDialog.getSaveFileName(self, "Save Text File", "", "Text File (*.txt)")
        files = self.list.selectedItems()

        f = open(self.saveFile, "w")

        for filePath in files:
            print filePath.text()
            f.write(str(filePath.text()))
            f.write("\n")
        f.close()

    def runBatch(self):
        python = self.script.text()
        files = self.list.selectedItems()
        melCmd = ('source dsBatchToolHandler; dsBatchTool "%s";' % str(python))

        for f in files:
            filename = f.text()
            logName = filename.rsplit("/",1)[-1].rsplit(".",1)[0]
            print logName
            logPath = "C:\\%s_log.txt" % logName.rsplit("/",1)[-1].rsplit(".",1)[0]
            #logPath = "C:/Test_log.txt"

            os.system("maya -batch -log '%s' -command '%s' -file '%s'" % (logPath, str(melCmd), filename))
            print "DONE"


#IF not runned inside Maya
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = dsVrayShapeAttr(parent=None)
    myapp.show()
    sys.exit(app.exec_())

def dsBatchToolUI():
    global myWindow
    myWindow = dsVrayShapeAttr(parent=getMayaWindow())
    myWindow.show()