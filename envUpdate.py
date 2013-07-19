import os,shutil

maya2012 = "C:/Users/admin/Documents/maya/2012-x64"
maya2013 = "C:/Users/admin/Documents/maya/2013-x64"
maya2014 = "C:/Users/admin/Documents/maya/2014-x64"

mayaList = [maya2012,maya2013,maya2014]

for maya in mayaList:
    if os.path.isdir(maya):
        
        yearSplit = maya.split("/")
        
        print "Updating maya "+ yearSplit[-1][:4] +" maya.env"
        
        envGlobal = "//vfx-data-server/dsGlobal/globalMaya/env/"+ yearSplit[-1][:4] +"/Maya_dsGlobal_windows.env"
        envSys = maya + "/Maya.env"
        shutil.copy(envGlobal,envSys)
        

oldDuck = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/DuckTools"
newDuck = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/_duckTools"
if os.path.isdir(oldDuck):os.rename(oldDuck,newDuck)

if os.path.isfile(oldDuck+"/maya2013.exe"):os.remove(oldDuck+"/maya2013.exe")

