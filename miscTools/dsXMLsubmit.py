import os,re,shutil

def getXML(rootPath,seq):

    keyList = []
    rlDict = {}
    seqPath = rootPath + "/" + seq
    tmpRenderFiles = os.listdir(seqPath+"/renderFiles")
    
    for file in tmpRenderFiles:
        if re.search(".xml",file):    
             if file[:-9] not in keyList:
                 keyList.append(file[:-9])
                 
    keyList.sort()
    for key in keyList:
        rlXML = []
        for file in tmpRenderFiles:
            if re.search(key,file):
                rlXML.append(file)
            rlDict[key] = rlXML

    for key in sorted(rlDict):
        xmlPath = seqPath + "/renderFiles/"+ rlDict[key][-1]
        reformatXML(xmlPath)
        
def reformatXML(path):
    xmlFile = open( path, 'r')
    list = xmlFile.readlines() 
    lines = filter(lambda x:not x.isspace(),list)
    xmlFile.close() 
      
    renderXml = path.replace(".xml","_clean.xml")
    rrFile = open(renderXml, 'w')
    
    for line in lines:
        if re.search("<SeqStart>",line):
            tmpVal = line.split("    ")
            val = tmpVal[1].split(".")[0]
            line = "    <SeqStart>    "+ val + "    </SeqStart>\n"
            
        if re.search("<SeqEnd>",line):   
            tmpVal = line.split("    ")
            val = tmpVal[1].split(".")[0]
            line = "    <SeqEnd>    "+ val + "    </SeqEnd>\n"
        
        if re.search("UserName",line):
            line = "    <UserName>    FRIENDS    </UserName>\n"
        if re.search("<ImageFileNameVariables>",line):
            tmpVal = line.split("    ")
        if re.search("<ImageDir>",line):
            tmpPath = line.split("    ")
            newPath = tmpPath[1].strip(" ") + tmpVal[1].strip(" ")[:-1]
            line = "    <ImageDir>    " + str(newPath) + "    </ImageDir>\n"
        if re.search("<RRO_AutoApproveJob>",line):
            line = "    <RRO_AutoApproveJob> false </RRO_AutoApproveJob>\n"
        if re.search("<Clients>",line):
            line = "    <Clients>    RFarm    </Clients>"
        rrFile.write(line)
    rrFile.close()

    shutil.copy(renderXml,"R:/autoload")



rootPath ="//vfx-data-server/dsPipe/Lego_Friends/film/LEGO_Friends_EP03_147768"
seq = "q0290"
getXML(rootPath,seq)