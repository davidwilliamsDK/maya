import os,re,shutil,fnmatch



def searchRef(filePath,localAssetPath,remoteAssetPath):

    file = filePath.split("/")[-1]
    file = file.strip("\n")
    file = file[:-2]
    
    print file
    print remoteAssetPath
    matches = []
    for root, dirnames, filenames in os.walk(remoteAssetPath):
      for filename in fnmatch.filter(filenames, file):
          matches.append(os.path.join(root, filename))
          break
      #print matches


def readRef(path,localAssetPath,remoteAssetPath):
    #print path
    refList = []
    maFile = open( path, 'r')
    list = maFile.readlines() 
    lines = filter(lambda x:not x.isspace(),list)
    maFile.close() 
    
    #newMA = path.replace(".ma","_newPaths.ma")
    #maFile = open(newMA, 'w')
    
    for line in lines:
        if re.search(".ma\";",line):
            searchRef(line,localAssetPath,remoteAssetPath)
            #lineSplit = line.split(" ")
            #newLine = line.replace("assets",localAssetPath)
            #maFile.write(newLine)
            #print newLine
            #try:
            #    if lineSplit[-1] not in refList:
            #        if not re.search("dsPipe",lineSplit[-1]):
                        #if re.search("asset",lineSplit[-1]):
            #            refList.append(lineSplit[-1])
            #except:
            #    pass
        #else:
        #    pass
            #maFile.write(line)
            #print line
    #maFile.close()
    #print newMA
    #refList.sort()
    #return refList

def refSync(path,remoteAssetPath,localAssetPath):
    
    localPath = path.replace("assets",localAssetPath)
    remotePath = path.replace("assets",remoteAssetPath)
    #print path
    #if os.path.isdir(localPath) == False:
        #print "coping " + remotePath + " to: " + localPath
        
        #shutil.copytree(remotePath,localPath)
    #else:
        #pass

def getRef(rootPath,remoteAssetPath,localAssetPath):
    refList = []
    masterList = []
    matches = []
    for root, dirnames, filenames in os.walk(rootPath):
      for filename in fnmatch.filter(filenames, '*.ma'):
          matches.append(os.path.join(root, filename))

    for match in matches:
        refList = readRef(match,localAssetPath,remoteAssetPath)
#
#        for path in refList:
#            path = path.strip(";")
#            path = path.strip("\n")
#            path = path.strip("\"")
#            pSplit = path.split("/")
#            path = path.replace("/" + pSplit[-1],"")
#            if path not in masterList:
#                masterList.append(path)
#
#    masterList.sort()
#    for path in masterList:
#        print path
#        refSync(path,remoteAssetPath,localAssetPath)


remoteAssetPath = "//192.168.0.71/chimasync/assets"
localAssetPath = "P:/Lego_ChimaFillers/asset"
rootPath ="//vfx-data-server/dsPipe/Lego_ChimaFillers/temp/locafill01_anim_files_pf_refs"
getRef(rootPath,remoteAssetPath,localAssetPath)