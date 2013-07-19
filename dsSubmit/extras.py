import os,re,shutil




def cleanFolders(path):
    shotList = os.listdir(path)

    for shot in shotList:
        if re.search("s[0-9][0-9][0-9][0-9]",shot):

            shotpath = path + "/" + shot + "/rawRender"
            try:
                rlList = os.listdir(shotpath)
                for rl in rlList:
                    print shot
                    print rl
                    rlPath = shotpath + "/" + rl
                    tmpList = os.listdir(rlPath)
                    topLvl = rlPath
                    if tmpList != []:
                        sndLvl = rlPath + "/" + tmpList[0]
                        try:
                            if os.path.isdir(sndLvl):
                                fileList = os.listdir(sndLvl)
                                for file in fileList:
                                    srcPath = sndLvl + "/" + file
                                    dstPath = topLvl + "/" + file
                                    print "moving " + rl
                                    #shutil.move(srcPath,dstPath)
                                    print srcPath
                                    print dstPath
                                    #os.remove(srcPath)
                        except:
                            pass

            except:
                pass

path = "//vfx-data-server/dsPipe/Lego_Friends/film/LEGO_Friends_EP03_147768/"
tmpList = os.listdir(path)
for tmp in tmpList:
    if re.search("q[0-9][0-9][0-9][0-9]",tmp):
        print path + "/" + tmp
        cleanFolders(path + "/" + tmp)

#cleanFolders(path)