#Import needed modules
import sys, os, re, shutil, random, sip, platform
from PyQt4 import QtCore, QtGui
import subprocess

#Custom import modules
from dsShotOpenUI import Ui_ShotOpenMainWindow
import dsCommon.dsOsUtil as dsOsUtil
reload(dsOsUtil)
import dsCommon.dsProjectUtil as dsProjectUtil
reload(dsProjectUtil)
import dsCommon.dsMayaEnv as dsMayaEnv
reload(dsMayaEnv)

#Import PyQt for Interface
from PyQt4.QtCore import *
from PyQt4.QtGui import *

if dsOsUtil.mayaRunning() == True:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMayaUI as mui

#If inside Maya open Maya GUI
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):

        #Setup Window
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ShotOpenMainWindow()
        self.ui.setupUi(self)

        #Init definitions to update UI
        MyForm.filmUpdate(self)

        #For action, run def
        QtCore.QObject.connect(self.ui.filmComboBox, QtCore.SIGNAL("activated(int)"), self.episodeUpdate);
        QtCore.QObject.connect(self.ui.folderListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.folderHandle);
        QtCore.QObject.connect(self.ui.folderListWidget, SIGNAL("itemClicked(QListWidgetItem *)"), self.listFiles);
        QtCore.QObject.connect(self.ui.fileListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.fileOpen);
        QtCore.QObject.connect(self.ui.fileListWidget, SIGNAL("itemClicked(QListWidgetItem *)"), self.exportComboUpdate);
        QtCore.QObject.connect(self.ui.exportPushButton, QtCore.SIGNAL("clicked()"), self.exportFile);
        QtCore.QObject.connect(self.ui.episodeComboBox, QtCore.SIGNAL("activated(int)"), self.seqFolderUpdate);

        #Set Context Menu for file list widget
        #self.ui.fileListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        #self.ui.fileListWidget.customContextMenuRequested.connect(self.fileListWidgetMenu);

        #self.ui.folderListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
        #self.ui.folderListWidget.customContextMenuRequested.connect(self.folderListWidgetMenu);

        #Gui Settings
        #self.settings = QtCore.QSettings("Duckling&Sonne", "dsShotOpen")
        #self.filmState = None
        self.seq = ""
        self.seqShotToggle = True

        #self.readSettings()
        if os.getenv('RELATIVEPATH') != None:
            self.readEnv()
            self.updateComboBox()

    def updateComboBox(self):
        print "updating to current env's"
        self.ui.filmComboBox.setCurrentIndex(self.ui.filmComboBox.findText(self.dsProject))
        self.episodeUpdate()
        self.ui.episodeComboBox.setCurrentIndex(self.ui.episodeComboBox.findText(self.dsEpisode))
        self.seqFolderUpdate()

    def readEnv(self):
        self.dsRelativePath = os.environ['RELATIVEPATH']
        self.dsProject = os.environ['PROJECT']
        self.dsEpisode = os.environ['EPISODE']
        self.dsSequence = os.environ['SEQUENCE']

    def testEnv(self):
        print "Testing Project Env's"
        if sys.platform == "linux2":
            dsMayaEnv.set_duckling_env()
        if sys.platform == "win32":
            dsMayaEnv.set_PC_duckling_env()


    def exportComboUpdate(self, item):
        typelist = ["Layout", "Blocking", "Anim", "Light", "Effect"]
        obj = str(item.text()).rsplit("_", 1)[-1].rsplit(".", 1)[0]

        if obj in typelist:
            index = typelist.index(obj) + 1

            if not index >= len(typelist):
                for i in range(index, len(typelist)):
                    self.ui.exportComboBox.addItem("")
                    self.ui.exportComboBox.setItemText(i-index, QtGui.QApplication.translate("ShotOpenMainWindow", typelist[i], None, QtGui.QApplication.UnicodeUTF8))
            else:
                self.ui.exportComboBox.addItem("")
                self.ui.exportComboBox.setItemText(0, QtGui.QApplication.translate("ShotOpenMainWindow", "Not Valid", None, QtGui.QApplication.UnicodeUTF8))

    def exportFile(self):
        '''Exporting file to next pipelinestep'''
        exportType = self.ui.exportComboBox.currentText()
        selFile = self.ui.fileListWidget.currentItem().text()
        seqPath = aiConfig.expandSetting("ai_ProductionShotPath")
        fullPath = self.ui.fileListWidget.currentItem().whatsThis()
        fileTypes = MyForm.getFileTypes(self)

        #Save scene if it's open before export
        if osUtil.mayaRunning() == True:
            curOpenFile = cmds.file(expandName=True, q=True)
            exportFile = "%s/%s" % (fullPath, selFile)
            if curOpenFile == exportFile:
                if cmds.file(q=True, anyModified=True):
                    message = "Scene is open! Save before export?"
                    MyForm.exportConfirmDialog(self, curOpenFile, True, False, message)

        if exportType:
            if not str(exportType) == "Not Valid":
                curType=None

                for fileType in fileTypes:
                    if fileType in selFile:
                        curType = fileType

                if curType:
                    seqPath = aiConfig.expandSetting("ai_ProductionShotPath")
                    fullPath = self.ui.fileListWidget.currentItem().whatsThis()

                    newPath = "%s/_%s" % (seqPath, exportType)

                    if not os.path.exists(newPath):
                        os.makedirs(newPath)
                    if os.path.exists(newPath):
                        shutil.copy("%s/%s" % (fullPath, selFile), "%s/%s" % (newPath, selFile.replace(curType, exportType)))
                        MyForm.listFiles(self)

            message = "Want to Open exported file?"
            MyForm.exportConfirmDialog(self, "%s/%s" % (newPath, selFile.replace(curType, exportType)), False, True, message)

    def filmUpdate(self):
        '''Update the film list'''
        i=0
        film = dsProjectUtil.listProjects()
        if "Library" in film:
            film.remove("Library")

        if film:
            for project in film:
                self.ui.filmComboBox.addItem("")
                self.ui.filmComboBox.setItemText(i, QtGui.QApplication.translate("ShotOpenMainWindow", project, None, QtGui.QApplication.UnicodeUTF8))
                i=i+1

        self.episodeUpdate()

    def episodeUpdate(self):
        self.ui.episodeComboBox.clear()
        i=0
        project = self.ui.filmComboBox.currentText()

        try:
            episodes = dsProjectUtil.listEpisodes(project)

            if episodes:
                for episode in episodes:
                    if not episode.startswith("."):
                        self.ui.episodeComboBox.addItem("")
                        self.ui.episodeComboBox.setItemText(i, QtGui.QApplication.translate("ShotOpenMainWindow", episode, None, QtGui.QApplication.UnicodeUTF8))
                        i=i+1

            self.seqFolderUpdate()
        except:
            pass

    def fileOpen(self, item=None):
        '''Opens the selected maya file'''
        print item.text()
        animSubFolders = dsProjectUtil.animPathList()

        project = self.ui.filmComboBox.currentText()
        episodes = self.ui.episodeComboBox.currentText()

        filePath = ""

        if self.seqShotToggle == True:
            filePath = "%s%s" % (dsProjectUtil.seqAnimPath(project, episodes, self.seq), item.text())
        else:
            filePath = "%s%s" % (dsProjectUtil.shotAnimPath(project, episodes, self.seq, item.text()), item.text())

        print filePath
        if dsOsUtil.mayaRunning():
            if cmds.file(q=True, anyModified=True):
                MyForm.saveConfirmDialog(self, filePath)
                print "save file"
            else:
                cmds.file(filePath, o=True )
        self.testEnv()

    def saveConfirmDialog(self, item, message=None):
        '''Save Dialog if file needs to be saved'''
        if not message:
            message = "Want to to Save, before closing?"

        reply = QtGui.QMessageBox.question(self, 'Message',
            message, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No| QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            cmds.file( save=True, type='mayaAscii' )
            cmds.file(item, o=True, f=True)
            self.ui.statusbar.showMessage("File saved - File opened")
        elif reply == QtGui.QMessageBox.No:
            cmds.file(item, o=True, f=True)
            self.ui.statusbar.showMessage("File opened")
        else:
            self.ui.statusbar.showMessage("Open Scene Cancled")

    def exportConfirmDialog(self, item, Save, Open, message=None):
        '''Export Dialog if file needs to be saved'''
        if not message:
            message = "Want to Save, before closing?"

        reply = QtGui.QMessageBox.question(self, 'Message',
            message, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No| QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if Save:
                cmds.file( save=True, type='mayaAscii' )
            if Open:
                cmds.file(item, o=True, f=True)
                self.ui.statusbar.showMessage("File saved - File opened")
        elif reply == QtGui.QMessageBox.No:
            pass
        else:
            if Open:
                self.ui.statusbar.showMessage("Open Scene Cancled")
            if not Open:
                self.ui.statusbar.showMessage("Operation Cancled")

    def folderHandle(self, item):
        self.ui.exportComboBox.clear()
        self.ui.fileListWidget.clear()
        if ".." in item.text():
            MyForm.seqFolderUpdate(self)
        elif self.seqShotToggle:
            MyForm.shotFolderUpdate(self, item.text())
            self.seqShotToggle = False
        else:
            MyForm.seqFolderUpdate(self)
            self.seqShotToggle = True


    def seqFolderUpdate(self):
        '''Update the folder list, with sequences'''

        project = self.ui.filmComboBox.currentText()
        episodes = self.ui.episodeComboBox.currentText()

        seqs = dsProjectUtil.seqList(project, episodes)
        self.ui.folderListWidget.clear()
        self.ui.fileListWidget.clear()

        i=0
        if seqs:
            for seq in seqs:
                self.ui.folderListWidget.addItem("")
                self.ui.folderListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow", seq, None, QtGui.QApplication.UnicodeUTF8))
                i=i+1

        self.seqShotToggle = True

    def shotFolderUpdate(self, item=None):
        '''Update the folder list, with shots'''
        project = self.ui.filmComboBox.currentText()
        episodes = self.ui.episodeComboBox.currentText()
        self.seq = item

        shots = dsProjectUtil.shotList(project, episodes, self.seq)
        self.ui.folderListWidget.clear()

        i=0
        if shots:
            for shot in shots:
                self.ui.folderListWidget.addItem("")
                self.ui.folderListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow", shot, None, QtGui.QApplication.UnicodeUTF8))
                i=i+1


    def listFiles(self, item=None):
        '''List all files in the animation diretories'''
        self.ui.fileListWidget.clear()
        self.ui.exportComboBox.clear()

        if not item:
            item = self.ui.folderListWidget.currentItem()

        if item:
            animSubFolders = dsProjectUtil.animPathList()

            project = self.ui.filmComboBox.currentText()
            episodes = self.ui.episodeComboBox.currentText()
            path = ""

            if self.seqShotToggle == True:
                self.seq = item.text()
                path = dsProjectUtil.seqAnimPath(project, episodes, self.seq)
            else:
                path = dsProjectUtil.shotAnimPath(project, episodes, self.seq, item.text())

            i=0
            if animSubFolders:
                if path:
                    for animSub in animSubFolders:
                        try:
                            for mafile in dsOsUtil.listMa("%s%s/" % (path,animSub)):
                                self.ui.fileListWidget.addItem("")
                                self.ui.fileListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow","%s/%s" % (animSub, mafile), None, QtGui.QApplication.UnicodeUTF8))
                                self.ui.fileListWidget.item(i).setWhatsThis(path)
                                i=i+1
                            for mbfile in dsOsUtil.listMb("%s%s/" % (path,animSub)):
                                self.ui.fileListWidget.addItem("")
                                self.ui.fileListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow","%s/%s" % (animSub, mbfile), None, QtGui.QApplication.UnicodeUTF8))
                                self.ui.fileListWidget.item(i).setWhatsThis(path)
                                i=i+1
                        except:
                            pass

        #Do it for shots too
        shotShots = dsProjectUtil.shotShotList(project, episodes, self.seq)
        print shotShots
        for shot in shotShots:
            path = dsProjectUtil.shotAnimPath(project, episodes, item.text(), shot)
            print path

            if animSubFolders:
                if path:
                    for animSub in animSubFolders:
                        try:
                            for mafile in dsOsUtil.listMa("%s%s/" % (path,animSub)):
                                self.ui.fileListWidget.addItem("")
                                self.ui.fileListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow","%s/%s/%s" % (shot, animSub, mafile), None, QtGui.QApplication.UnicodeUTF8))
                                self.ui.fileListWidget.item(i).setWhatsThis(path)
                                i=i+1
                            for mbfile in dsOsUtil.listMb("%s%s/" % (path,animSub)):
                                self.ui.fileListWidget.addItem("")
                                self.ui.fileListWidget.item(i).setText(QtGui.QApplication.translate("AssetWindow","%s/%s/%s" % (shot, animSub, mbfile), None, QtGui.QApplication.UnicodeUTF8))
                                self.ui.fileListWidget.item(i).setWhatsThis(path)
                                i=i+1
                        except:
                            pass


    def folderListWidgetMenu(self, position):
        menu = QMenu()
        selectedItem = self.ui.folderListWidget.currentItem()

        if selectedItem:
            #If Sequence
            if self.seqShotToggle:
                path = aiConfig.expandSetting("ai_ProductionShotPath").split("/")
                path = ("\\").join(path)
                previewPath = aiConfig.expandSetting("ai_ProductionSequencePreviewPath").split("/")
                previewPath = ("\\").join(previewPath)

##            #If Shot
##            if not self.seqShotToggle:
##                path = aiConfig.expandSetting("ai_ProductionFilePath").split("/")
##                path = ("\\").join(path)
##                previewPath = aiConfig.expandSetting("ai_ProductionShotPreviewPath").split("/")
##                previewPath = ("\\").join(previewPath)

##            movfiles = self.listMOV(previewPath)
##            print movfiles
##            if movfiles:
##                previewMenu = menu.addMenu("Shot Preview")
##                for item in movfiles:
##                    entry = previewMenu.addAction(item)
##                    self.connect(entry,QtCore.SIGNAL('triggered()'), lambda item=item: self.openMov(previewPath, item=item))
##                    previewMenu.addAction(entry)

            exploreAction = menu.addAction("Open in Explore")
            quitAction = menu.addAction("Quit")
            action = menu.exec_(self.ui.folderListWidget.mapToGlobal(position))

            #Check Action
            if action == quitAction:
                self.exitWidget()
            if action == exploreAction:
                self.openAssetExplore(path)


    def openMov(self, path, item):
        moviePath = "%s\\%s" % (path, item)
        if os.path.exists(path):
            playerPath = "C:\Program Files (x86)\QuickTime\QuickTimePlayer.exe"
            if os.path.exists(playerPath):
                subprocess.Popen([playerPath, moviePath])


    def listMOV(self, path):
        Mov = []
        if os.path.exists(path) == True:
            for item in os.listdir(path):
                if "." in item:
                    ext = item.rsplit(".", 1)[1].lower()
                    acceptedExt = ["mov", "avi"]
                    if ext in acceptedExt:
                        Mov.append(item)
        else:
            Mov = None
        if Mov == []:
            Mov = None

        return Mov

    def exitWidget(self):
        if dsOsUtil.mayaRunning() == True:
            global dsShotOpenForm
            self.ui.statusbar.showMessage('Quitting')
            mel.eval('print "DS Shot Open Dialog closed"')
            dsShotOpenForm.close()
        else:
            self.close()

    def fileListWidgetMenu(self, position):
        menu = QMenu()
        selectedItem = self.ui.fileListWidget.currentItem()
        if selectedItem:
            openAction = ""
            openAction = menu.addAction("Open File")
            quitAction = menu.addAction("Quit")
            exploreAction = menu.addAction("Open in Explore")
            action = menu.exec_(self.ui.fileListWidget.mapToGlobal(position))

            #Check Action
            if action == quitAction:
                self.exitWidget()
            if action == exploreAction:
                path = self.ui.fileListWidget.currentItem().whatsThis().split("/")
                path = path.join("\\")
                self.openAssetExplore(path)
            if action == openAction:
                self.fileOpen()

    def openAssetExplore(self, path=None):
        if path:
            if os.path.exists(path):
                subprocess.Popen("explorer %s" % (path))
            else:
                self.ui.statusbar.showMessage("Path dosen't exist")

    def closeEvent(self, event):
        '''The close event makes sure to save gui settings'''
        MyForm.writeSettings(self)
        event.accept()


    def readSettings(self):
        '''Read application settings from the QT Settings object.'''
        settings = QtCore.QSettings("Duckling&Sonne", "dsShotOpen")

        self.filmState = settings.value("filmState").toString()
        if self.filmState:
            self.ui.filmComboBox.setCurrentIndex(self.ui.filmComboBox.findText(self.filmState))
            MyForm.seqFolderUpdate(self)


    def writeSettings(self):
        '''Write application settings'''
        settings = QtCore.QSettings("Duckling&Sonne", "dsShotOpen")
        settings.setValue("filmState", self.ui.filmComboBox.currentText())

    def set_env(self, env, arg):
        '''Set environment variable'''
        os.environ[str(env)] = '%s' % arg

def UI():
    global dsShotOpenForm
    dsShotOpenForm = MyForm(getMayaWindow())
    dsShotOpenForm.show()