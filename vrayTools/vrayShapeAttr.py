import os,sys,sip
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import maya.mel as mel
import dsCommon.dsProjectUtil as projectUtil
reload(projectUtil)

#Decalring Paths
dev = "dsDev"
live = "dsGlobal"
status = live

guiName = "vrayShapeAttrGUI.ui"
clashNameSpace = "CLASSINGELEMENT_"

if sys.platform == "linux2":
    uiFile = '/' + status +  '/dsCore/maya/vrayTools/%s' % guiName
else:
    if status == live:
        server = projectUtil.listGlobalPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/vrayTools/%s' % guiName
    else:
        server = projectUtil.listDevPath()
        sys.path.append(server + '/dsCore/maya/dsCommon/')
        uiFile = server + '/dsCore/maya/vrayTools/%s' % guiName

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
    def __init__(self, parent=getMayaWindow()):
        super(base_class, self).__init__(parent)
        self.setupUi(self)

        self.add.clicked.connect(self.addAttr)
        self.remove.clicked.connect(self.removeAttr)

        #Connecting buttons
        self.subdivision.clicked.connect(self.subdivisionAttr)
        self.disQuality.clicked.connect(self.disQualityAttr)
        self.disControl.clicked.connect(self.disControlAttr)
        self.roundEdges.clicked.connect(self.roundEdgesAttr)
        self.userAttr.clicked.connect(self.userAttrAttr)
        self.fogFade.clicked.connect(self.fogFadeAttr)
        self.objectID.clicked.connect(self.objectIDAttr)
        self.subDiv_render.clicked.connect(self.subDiv_Attr)
        self.subDiv_uv.clicked.connect(self.subDiv_uvAttr)
        self.disQuality_override.clicked.connect(self.disQualitySubAttr)
        self.round_round.clicked.connect(self.roundEdgesSubAttr)
        self.dis_none.clicked.connect(self.disControlTypeAttr)
        self.dis_waterLevel.clicked.connect(self.disControlWaterAttr)
        self.dis_type.activated.connect(self.disControlTypeDropdown)
        self.dis_filter.clicked.connect(self.disControlFilterAttr)
        self.dis_boundsDropdown.activated.connect(self.disControlBoundsAttr)

        #Initialise Settings Attr
        self.subdivisionAttr()
        self.disQualityAttr()
        self.disControlAttr()
        self.fogFadeAttr()
        self.roundEdgesAttr()
        self.objectIDAttr()
        self.userAttrAttr()

    def addAttr(self):
        onOff = 1
        self.vrayAttr(onOff)
    def removeAttr(self):
        onOff = 0
        self.vrayAttr(onOff)

    #CONTROL ATTRIBUTES ENABLE/DISABLE
    def subdivisionAttr(self):
        if self.subdivision.checkState() == 2: state=True
        else: state=False
        self.subDiv_render.setEnabled(state)
        self.subDiv_Attr()

    def subDiv_Attr(self):
        if self.subdivision.checkState() == 2:
            if self.subDiv_render.checkState() == 2: state=True
            else: state=False
        else: state=False
        self.subDiv_uv.setEnabled(state)
        self.subDiv_static.setEnabled(state)
        self.subDiv_uvAttr()

    def subDiv_uvAttr(self):
        if self.subdivision.checkState() == 2:
            if self.subDiv_render.checkState() == 2:
                if self.subDiv_uv.checkState() == 2: state=True
                else: state=False
            else: state=False
        else: state=False
        self.subDiv_borders.setEnabled(state)

    def disQualityAttr(self):
        if self.disQuality.checkState() == 2: state=True
        else: state=False
        self.disQuality_override.setEnabled(state)
        self.disQualitySubAttr()

    def disQualitySubAttr(self):
        if self.disQuality.checkState() == 2:
            if self.disQuality_override.checkState() == 2: state=True
            else: state=False
        else: state=False
        self.disQuality_edge.setEnabled(state)
        self.disQuality_edgeLabel.setEnabled(state)
        self.disQuality_edgeSlider.setEnabled(state)
        self.disQuality_max.setEnabled(state)
        self.disQuality_maxLabel.setEnabled(state)
        self.disQuality_maxSlider.setEnabled(state)
        self.disQuality_view.setEnabled(state)

    def disControlAttr(self):
        if self.disControl.checkState() == 2: state=True
        else: state=False
        self.dis_none.setEnabled(state)
        self.disControlTypeAttr()

    def disControlTypeAttr(self):
        if self.disControl.checkState() == 2:
            if self.dis_none.checkState() == 0: state=True
            else: state=False
        else: state=False
        self.dis_type.setEnabled(state)
        self.dis_typeLabel.setEnabled(state)
        self.dis_amount.setEnabled(state)
        self.dis_amountLabel.setEnabled(state)
        self.dis_amountSlider.setEnabled(state)
        self.dis_shift.setEnabled(state)
        self.dis_shiftLabel.setEnabled(state)
        self.dis_shiftSlider.setEnabled(state)
        self.dis_continuity.setEnabled(state)
        self.dis_waterLevel.setEnabled(state)
        self.dis_filter.setEnabled(state)

        self.disControlWaterAttr()
        self.disControlTypeDropdown()
        self.disControlFilterAttr()

    def disControlWaterAttr(self):
        if self.disControl.checkState() == 2:
            if self.dis_none.checkState() == 0:
                if self.dis_waterLevel.checkState() == 2: state=True
                else: state=False
            else: state=False
        else: state=False
        self.dis_waterAmount.setEnabled(state)
        self.dis_waterAmountLabel.setEnabled(state)
        self.dis_waterAmountSlider.setEnabled(state)

    def disControlTypeDropdown(self):
        if self.disControl.checkState() == 2:
            if self.dis_none.checkState() == 0:
                if self.dis_type.currentIndex() == 0: state=True
                else: state=False
            else: state=False
        else: state=False
        self.dis_precision.setEnabled(state)
        self.dis_precisionLabel.setEnabled(state)
        self.dis_precisionSlider.setEnabled(state)
        self.dis_texture.setEnabled(state)
        self.dis_textureLabel.setEnabled(state)
        self.dis_textureSlider.setEnabled(state)
        self.dis_bounds.setEnabled(state)

        if self.disControl.checkState() == 2:
            if self.dis_none.checkState() == 0:
                if state==True: state=False
                else: state=True
            else: state=False
        else: state=False
        self.dis_boundsDropdown.setEnabled(state)
        self.dis_boundsDropdownLabel.setEnabled(state)
        self.disControlBoundsAttr()

    def disControlFilterAttr(self):
        if self.disControl.checkState() == 2:
            if self.dis_none.checkState() == 0:
                if self.dis_filter.checkState() == 2: state=True
                else: state=False
            else: state=False
        else: state=False
        self.dis_filterblur.setEnabled(state)
        self.dis_filterblurLabel.setEnabled(state)
        self.dis_filterblurSlider.setEnabled(state)

    def disControlBoundsAttr(self):
        if self.disControl.checkState() == 2:
            if self.dis_type.currentIndex() != 0:
                if self.dis_boundsDropdown.currentIndex() == 1: state=True
                else: state=False
            else: state=False
        else: state=False
        self.dis_boundsMax.setEnabled(state)
        self.dis_boundsMaxLabel.setEnabled(state)
        self.dis_boundsMaxSlider.setEnabled(state)
        self.dis_boundsMin.setEnabled(state)
        self.dis_boundsMinLabel.setEnabled(state)
        self.dis_boundsMinSlider.setEnabled(state)


    def roundEdgesAttr(self):
        if self.roundEdges.checkState() == 2: state=True
        else: state=False
        self.round_round.setEnabled(state)
        self.roundEdgesSubAttr()

    def roundEdgesSubAttr(self):
        if self.roundEdges.checkState() == 2:
            if self.round_round.checkState() == 2: state=True
            else: state=False
        else: state=False
        self.round_radius.setEnabled(state)
        self.round_radiusSlider.setEnabled(state)
        self.round_radiusLabel.setEnabled(state)

    def userAttrAttr(self):
        if self.userAttr.checkState() == 2: state=True
        else: state=False
        self.user_attr.setEnabled(state)
        self.user_attrLabel.setEnabled(state)

    def fogFadeAttr(self):
        if self.fogFade.checkState() == 2: state=True
        else: state=False
        self.fog_radius.setEnabled(state)
        self.fog_radiusLabel.setEnabled(state)
        self.fog_radiusSlider.setEnabled(state)

    def objectIDAttr(self):
        if self.objectID.checkState() == 2: state=True
        else: state=False
        self.obj_id.setEnabled(state)
        self.obj_idLabel.setEnabled(state)
        self.obj_idSlider.setEnabled(state)

    #ACTUAL FUNCTION
    def vrayAttr(self, onOff):
        sel = cmds.ls(sl=True)
        shapes = cmds.listRelatives(sel, ad=True, fullPath=True, type=["mesh", "nurbsSurface", "subdiv"])
        for shape in shapes:
            if self.subdivision.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_subdivision %s" % (shape, onOff))
                if onOff == 1:
                    if self.subDiv_render.checkState() == 2:
                        cmds.setAttr("%s.vraySubdivEnable" % shape, 1)
                        if self.subDiv_uv.checkState() == 2:
                            cmds.setAttr("%s.vraySubdivUVs" % shape, 1)
                            if self.subDiv_borders.checkState() == 2: cmds.setAttr("%s.vraySubdivUVsAtBorders" % shape, 1)
                            else: cmds.setAttr("%s.vraySubdivUVsAtBorders" % shape, 0)
                        else: cmds.setAttr("%s.vraySubdivUVs" % shape, 0)
                        if self.subDiv_static.checkState() == 2: cmds.setAttr("%s.vrayStaticSubdiv" % shape, 1)
                        else: cmds.setAttr("%s.vrayStaticSubdiv" % shape, 0)
                    else:
                        cmds.setAttr("%s.vraySubdivEnable" % shape, 0)
            if self.disQuality.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_subquality %s" % (shape, onOff))
                if onOff == 1:
                    if self.disQuality_override.checkState() == 2:
                        cmds.setAttr("%s.vrayOverrideGlobalSubQual" % shape, 1)

                        if self.disQuality_view.checkState() == 2: cmds.setAttr("%s.vrayViewDep" % shape, 1)
                        else: cmds.setAttr("%s.vrayViewDep" % shape, 0)
                        cmds.setAttr("%s.vrayEdgeLength" % shape, float(self.disQuality_edge.text()))
                        cmds.setAttr("%s.vrayMaxSubdivs" % shape, int(self.disQuality_max.text()))
                    else: cmds.setAttr("%s.vrayOverrideGlobalSubQual" % shape, 0)

            if self.disControl.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_displacement %s" % (shape, onOff))
                if onOff == 1:
                    if self.dis_none.checkState() != 2:
                        cmds.setAttr("%s.vrayDisplacementNone" % shape, 0)
                        cmds.setAttr("%s.vrayDisplacementType" % shape, int(self.dis_type.currentIndex()))
                        cmds.setAttr("%s.vrayDisplacementAmount" % shape, float(self.dis_amount.text()))
                        cmds.setAttr("%s.vrayDisplacementShift" % shape, float(self.dis_shift.text()))
                        if self.dis_continuity.checkState() != 2: cmds.setAttr("%s.vrayDisplacementKeepContinuity" % shape, 1)
                        else: cmds.setAttr("%s.vrayDisplacementKeepContinuity" % shape, 0)

                        if self.dis_waterLevel.checkState() != 2:
                            cmds.setAttr("%s.vrayEnableWaterLevel" % shape, 1)
                            cmds.setAttr("%s.vrayWaterLevel" % shape, float(self.dis_waterAmount.text()))
                        else: cmds.setAttr("%s.vrayEnableWaterLevel" % shape, 0)

                        print self.dis_type.currentIndex()
                        if self.dis_type.currentIndex() == 0:
                            cmds.setAttr("%s.vray2dDisplacementResolution" % shape, int(self.dis_texture.text()))
                            cmds.setAttr("%s.vray2dDisplacementPrecision" % shape, int(self.dis_precision.text()))
                            if self.dis_bounds.checkState() == 2: cmds.setAttr("%s.vray2dDisplacementTightBounds" % shape, 1)
                            else: cmds.setAttr("%s.vray2dDisplacementTightBounds" % shape, 0)

                        if self.dis_filter.checkState() == 2:
                            cmds.setAttr("%s.vray2dDisplacementFilterTexture" % shape, 1)
                            cmds.setAttr("%s.vray2dDisplacementFilterBlur" % shape, float(self.dis_filterblur.text()))
                        else: cmds.setAttr("%s.vray2dDisplacementFilterTexture" % shape, 0)

                        if self.dis_type.currentIndex() != 0:
                            if self.dis_boundsDropdown.currentIndex() == 1:
                                cmds.setAttr("%s.vrayDisplacementUseBounds" % shape, 1)
##                                cmds.setAttr("%s.vray2dDisplacementFilterBlur" % shape, float(self.dis_filterblur.text()))
##                                setAttr "pPlaneShape1.vrayDisplacementMinValue" -type double3 0.404501 0.404501 0.404501 ;
##                                setAttr "pPlaneShape1.vrayDisplacementMaxValue" -type double3 0.584268 0.584268 0.584268 ;
                            else: cmds.setAttr("%s.vrayDisplacementUseBounds" % shape, 0)
                    else:cmds.setAttr("%s.vrayDisplacementNone" % shape, 1)

            if self.roundEdges.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_roundedges %s" % (shape, onOff))
                if onOff == 1:
                    if self.round_round.checkState() == 2:
                        cmds.setAttr("%s.vrayRoundEdges" % shape, 1)
                        val = self.round_radius.text()
                        cmds.setAttr("%s.vrayRoundEdgesRadius" % shape, float(val))
                    else: cmds.setAttr("%s.vrayRoundEdges" % shape, 0)
            if self.userAttr.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_user_attributes %s" % (shape, onOff))
                if onOff == 1:
                    text = self.user_attr.text()
                    cmds.setAttr("%s.vrayUserAttributes" % shape, text, type="string")

            if self.fogFade.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_fogFadeOut %s" % (shape, onOff))
                if onOff == 1:
                    val = self.fog_radius.text()
                    cmds.setAttr("%s.vrayFogFadeOut" % shape, float(val))
            if self.objectID.checkState() == 2:
                mel.eval("vray addAttributesFromGroup %s vray_objectID %s" % (shape, onOff))
                if onOff == 1:
                    cmds.setAttr("%s.vrayObjectID" % shape, int(self.obj_id.text()))

def vrayShapeAttrUI():
    global myWindow
    myWindow = dsVrayShapeAttr()
    myWindow.show()