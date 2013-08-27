import os, shutil, platform
import distutils
import maya.mel as mel

version = mel.eval("about -version")
version = version.replace(" ", "-")
user = os.environ.get("USERNAME")

if platform.system() == "Windows":
    source = "//vfx-data-server/dsGlobal/globalMaya/presets/MAYA_PRESET_PATH/"
    destination = "C:/Users/%s/Documents/maya/%s/presets/" % (user, version)
    vScriptSrc = "//vfx-data-server/dsGlobal/globalMaya/Resources/vray_scripts/"
    vScriptDst = "C:/Program Files/Autodesk/Maya%s/vray/scripts/" % (version.split("-",1)[0])

elif platform.system() == "Linux":
    source = "/dsGlobal/globalMaya/presets/MAYA_PRESET_PATH/"
    destination = "/home/%s/maya/%s/presets/" % (user, version)
    vScriptSrc = "/dsGlobal/globalMaya/Resources/vray_scripts/"
    vScriptDst = "/usr/autodesk/maya%s/vray/scripts/" % (version)

def copyMayaPresets():
    copyFiles(source, destination)

def copyVrayScripts():
    copyFiles(vScriptSrc, vScriptDst)

def copyFiles(src, dst):
    data = []
    for path, subdirs, files in os.walk(src):
        for name in files:
            data.append(os.path.join(path, name))

    for d in data:
        if not os.path.exists("%s/%s" % (dst, d.rsplit("/",1)[-1])):
            dst = "%s%s" % (dst, d.rsplit("/",1)[-1])
            dst = dst.replace('\\', '/')
            if not os.path.exists(dst.rsplit("/",1)[0]):
                os.makedirs("%s/" % dst.rsplit("/",1)[0])
            shutil.copy2(d, dst)
        if os.path.exists("%s/%s" % (dst, d.rsplit("/",1)[-1])):
            dst = "%s%s" % (dst, d.rsplit("/",1)[-1])
            os.remove(dst)
            shutil.copy2(d, dst)