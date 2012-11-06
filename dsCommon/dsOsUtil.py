import os
import platform
import subprocess

def listFolder(path, exception=["_", "-", "."]):
    print path
    dirs = []
    try:
        for item in [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) if not d[0] in exception]:
            dirs.append(item)
        return sorted(dirs)
    except:
        return dirs

def listMa(path):
    dirs = []
    if os.path.exists(path) == True:
        for item in os.listdir(path):
            try:
                if item.split(".")[-1].lower() == "ma":
                    dirs.append(item)
            except:
                pass
        return sorted(dirs)
    else:
        return None

def listMb(path):
    dirs = []
    if os.path.exists(path) == True:
        for item in os.listdir(path):
            try:
                if item.split(".")[-1].lower() == "mb":
                    dirs.append(item)
            except:
                pass
        return sorted(dirs)
    else:
        return None

def mayaRunning():
    isMayaRunning = True
    try:
        import maya.cmds as cmds
    except:
        isMayaRunning = False
    return isMayaRunning

def readReplaceMa(filePath, oldArray, newArray):
    """Read Replace Text in MA file"""
    print "Running read replace ma"
    f = open(filePath, "r+")
    lines = f.readlines()
    doc = []

    for line in lines:
        for i in range(len(oldArray)):
            if oldArray[i] in line:
                line = line.replace(oldArray[i], newArray[i])
        doc.append(line)

    f.close()

    f = open(filePath, "w")
    for line in doc:
        f.write(line)
    f.close()

def listOS():
    return platform.system()

def openInBrowser(path):
    '''Open path in finder or Explorer'''
    currentOs = listOS()
    platform = str(currentOs)
    print path
    if platform == "Windows":
        print os.path.exists(path)
        if os.path.exists(path):
            path = path.split("/")
            path = path.join("\\")
            subprocess.Popen("explorer %s" % (path))
        else:
            self.ui.statusbar.showMessage("Path dosen't exist")
    if platform == "Linux":
        print "Linux"
        if os.path.exists(path):
            subprocess.Popen(["nautilus", path])
        else:
            self.ui.statusbar.showMessage("Path dosen't exist")