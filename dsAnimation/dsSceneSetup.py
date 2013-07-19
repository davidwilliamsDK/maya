import sys, os, re, shutil, imp

if sys.platform == "linux2":
    uiFile = '/dsGlobal/dsCore/maya/dsAnimation/dsSceneSetup.ui.ui'
    sys.path.append("/dsGlobal/dsGlobal/dsCore/maya")
    sys.path.append('/dsGlobal/dsCore/shotgun/')
else:
    uiFile = '//vfx-data-server/dsGlobal/dsCore/maya/dsAnimation/dsSceneSetup.ui'
    sys.path.append("//vfx-data-server/dsGlobal/dsCore/maya")
    sys.path.append('//vfx-data-server/dsGlobal/dsCore/shotgun/')

from PyQt4 import QtGui, QtCore, uic
import sgTools
import dsAnimSG as animSG
import dsAnimSetup as animSetup
reload(sgTools)
reload(animSG)

import dsCommon.dsProjectUtil as projectUtil

print 'Loading ui file:', os.path.normpath(uiFile)
form_class, base_class = uic.loadUiType(uiFile)

class MyForm(base_class, form_class):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        super(base_class, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('dsSceneSetup')
        self.setWindowTitle("dsSceneSetup")

        #SIGNALS
        QtCore.QObject.connect(self.project, QtCore.SIGNAL("activated(int)"), self.updateEpisodes);
        QtCore.QObject.connect(self.episode, QtCore.SIGNAL("activated(int)"), self.updateSequences);
        QtCore.QObject.connect(self.createSeq, QtCore.SIGNAL("clicked()"), self.runSeqCreate)

        self.updateProjects()

    def updateProjects(self):
        '''This Def list all project in the project dir, with a config.xml file in the root'''
        self.project.clear()
        projects = projectUtil.listProjects()
        print projects
        i = 0
        if projects:
            for project in projects:
                if i is 0:
                    self.project.addItem("")
                    self.project.setItemText(i, QtGui.QApplication.translate("MainWindow", "Select Project", None, QtGui.QApplication.UnicodeUTF8))
                    i = i+1
                self.project.addItem("")
                self.project.setItemText(i, QtGui.QApplication.translate("MainWindow", project, None, QtGui.QApplication.UnicodeUTF8))
                i = i+1

    def updateEpisodes(self):
        self.episode.clear()
        project = self.project.currentText()

        if not str(project) == "Select Episode":
            episodes = projectUtil.listEpisodes(project)
            print episodes
            i = 0
            if episodes:
                for episode in episodes:
                    if i is 0:
                        self.episode.addItem("")
                        self.episode.setItemText(i, QtGui.QApplication.translate("MainWindow", "Select Episode", None, QtGui.QApplication.UnicodeUTF8))
                        i = i+1
                    self.episode.addItem("")
                    self.episode.setItemText(i, QtGui.QApplication.translate("MainWindow", episode, None, QtGui.QApplication.UnicodeUTF8))
                    i = i+1

            if not str(self.episode.currentText()) == "Select Episode":
                self.updateSequences()

    def updateSequences(self):
        self.sequences.clear()
        project = self.project.currentText()
        episode = self.episode.currentText()

        if not str(episode) == "Select Episode":
            seqs = animSG.getEspisodeSequence(str(project), str(episode))
            item = QtGui.QListWidgetItem(self.sequences)

            i = 0
            for seq in seqs:
                self.sequences.addItem("")
                self.sequences.item(i).setText(QtGui.QApplication.translate("MainWindow", "%s_%s" % (str(seq['name']), str(seq['id'])), None, QtGui.QApplication.UnicodeUTF8))
                i = i+1

    def runSeqCreate(self):
        projInfo = {}
        projInfo['projName'] = str(self.project.currentText())
        projInfo['episode'] = str(self.episode.currentText())

        if not str(projInfo['projName']) == "Select Episode":
            if not str(projInfo['episode']) == "Select Episode":
                sequences = self.sequences.selectedItems()

                if sequences:
                    sequencesText = []

                    for seq in sequences:
                        print seq.text()
                        sequencesText.append(str(seq.text()))

                    if not sequencesText == []:
                        projInfo['sequences'] = sequencesText
                        animSetup.launch(projInfo)
        else:
            animSetup.launch(projInfo)
            print "Run Hole Sequence!!!"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())