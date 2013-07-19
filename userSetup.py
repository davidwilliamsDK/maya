import maya.cmds as cmds
import maya.mel as mel
import os, sys,threading

#sys.path.append('//vfx-data-server/dsGlobal/globalResources/Shotgun')
#from shotgun_api3 import Shotgun

print "THIS IS RUNNING A USERSETUP.PY FILE"

try:
  import vxmaya_setup
  import vxmaya_file
  import vxmaya_core
except:
  pass

mel.eval("evalDeferred dsMenu;")
#mel.eval("evalDeferred overwriteProc;")

if sys.platform == "win32":
    cmds.dirmap( en=True )
    cmds.dirmap( m=('/dsPipe/', '\\\\vfx-data-server\\dsPipe\\') )
    presetPath = "//vfx-data-server/dsGlobal/globalMaya/presets/"
    dest = "C:/Users/admin/Documents/maya/2013-x64/presets"

else:
    cmds.dirmap( en=True )
    cmds.dirmap( m=('\\\\vfx-data-server\\dsPipe\\','/dsPipe/') )
    cmds.dirmap( m=('P:\\','/dsPipe/') )
    presetPath = "/dsGlobal/globalMaya/presets/"
    dest = "/home/admin/maya/2013-x64/presets"
    
try:
    presetList = os.listdir(presetPath + "renderPreset")
    
    for rp in presetList:
        path = presetPath + "renderPreset" + "/" + rp
        shutil.copy(path,dest)
except:
    print "could not copy render presets to your machine"