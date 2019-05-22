#!/usr/bin/env python2.7
"""
For Maya 2016
Custom tools by James
__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import smartCombine
import uvui
import smartExtract
import faceCut
import unsmooth
import curveTube
import replaceTopo
import removeNamespaces
import imagePlaneToggle
import dualToggle
import camClipToggle


def smartcombine(arg=None):
    reload(smartCombine)
    smartCombine.smartCombine()

def smartextract(arg=None):
    reload(smartExtract)
    smartExtract.smartExtract()

def smartduplicate(arg=None):
    reload(smartExtract)
    smartExtract.smartDuplicate()

def facecut(arg=None):
    reload(faceCut)
    faceCut.faceCut()

def uvui_method(arg=None):
    reload(uvui)
    uvui.uvui().launch()

def unsmooth_method(arg=None):
    reload(unsmooth)
    unsmooth.unsmooth()

def curvetube(arg=None):
    reload(curveTube)
    curveTube.curveTube()

def replacetopo(arg=None):
    reload(replaceTopo)
    replaceTopo.replaceTopo().launch()

def remove_namespaces(arg=None):
    reload(removeNamespaces)
    removeNamespaces.removeNamespaces()

def imageplanetoggle(arg=None):
    reload(imagePlaneToggle)
    imagePlaneToggle.imagePlaneToggle()

def dualtoggle(arg=None):
    reload(dualToggle)
    dualToggle.dualToggle_on()

def camcliptoggle(arg=None):
    reload(camClipToggle)
    camClipToggle.camClipToggle()

def polyretopo(self, *args):
    cmds.polyRetopo()

def polyremesh(self, *args):
    cmds.polyRemesh()

def polymirrorcut(self, *args):
    mel.eval('polyMirrorCut 1 1 0.001;')

def polysel_every_n(self, *args):
    mel.eval('polySelectEdgesEveryN "edgeRing" 2;')

def assetToolsGUI():

    if cmds.dockControl("asset_tools_Collection_dock", exists=True):
        cmds.deleteUI("asset_tools_Collection_dock")

    dock_ui = cmds.window ("james_tools_gui",widthHeight=(200,150),
                              title="Asset Tools Collections",iconName="Asset Tools Collections",
                              resizeToFitChildren=True,minimizeButton=True)
    top_column = cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(numberOfColumns=2, parent=top_column)
    cmds.text(label="", width=65)
    cmds.symbolButton(image="jtools_icon.png", w=48, h=48)
    cmds.setParent('..')

    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0),
                                                 (tabs, 'bottom', 0), (tabs, 'right', 0)))
    allowedAreas = ['right','left']
    cmds.dockControl("asset_tools_Collection_dock",area='right',
                     content=dock_ui,
                     allowedArea=allowedAreas,
                     label='James Tools',
                     visible=True)
    bh = 24
    bw = 140
    ic = 34

#######################################################################
    main_column = cmds.columnLayout()
    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="uvui_icon.png", w=ic, h=ic, c="import uvui\nuvui.uvui().launch()")
    cmds.button(label="UV UI", w=bw, h=bh, c=uvui_method)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="facecut_icon.png", w=ic, h=ic, c="import faceCut\nfaceCut.faceCut()")
    cmds.button(l='FaceCut', w=bw, h=bh, c=facecut)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="combine_icon.png", w=ic, h=ic, c="import smartCombine\nsmartCombine.smartCombine()")
    cmds.button(label="Smart Combine", w=bw, h=bh, c=smartcombine)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="duplicate_icon.png", w=ic, h=ic, c="import smartExtract\nsmartExtract.smartDuplicate()")
    cmds.button(label="Smart Duplicate", w=bw, h=bh, c=smartduplicate)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="extract_icon.png", w=ic, h=ic, c="import smartExtract\nsmartExtract.smartExtract()")
    cmds.button(label="Smart Extract", w=bw, h=bh, c=smartextract)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="curvetube_icon.png", w=ic, h=ic, c="import curveTube\ncurveTube.curveTube()")
    cmds.button(label="CurveTube", w=bw, h=bh, c=curvetube)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="unsmooth_icon.png",w=ic, h=ic, c="import unsmooth\nunsmooth.unsmooth()")
    cmds.button(label="Unsmooth", w=bw, h=bh, c=unsmooth_method)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="replace_icon.png",w=ic, h=ic, c="import replaceTopo\nreplaceTopo.replaceTopo().launch()")
    cmds.button(label="Replace Topology", w=bw, h=bh, c=replacetopo)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="nameSpace_icon.png", w=ic, h=ic,
                     c="import removeNamespaces\nremoveNamespaces.removeNamespaces()")
    cmds.button(label="Remove Namespaces", w=bw, h=bh, c=remove_namespaces)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="dualTog_icon.png", w=ic, h=ic, c=dualtoggle,
                     doubleClickCommand="import dualToggle\ndualToggle.dualToggle_off()")
    cmds.button(label="Dual Toggle", w=bw, h=bh, c=dualtoggle)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="camTog_icon.png", w=ic, h=ic,
                     c="import imagePlaneToggle\nimagePlaneToggle.imagePlaneToggle()")
    cmds.button(label="Imageplane Toggle", w=bw, h=bh, command=imageplanetoggle)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
    cmds.shelfButton(i="clipToggle_icon.png", w=ic, h=ic,
                     c="import camClipToggle\ncamClipToggle.camClipToggle()")
    cmds.button(label="CamClip Toggle", w=bw, h=bh, command=camcliptoggle)
    cmds.setParent('..')
    cmds.setParent('..')

    maya_column = cmds.columnLayout()
    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=maya_column)
    cmds.shelfButton(i="commandButton.png", w=ic, h=ic, iol="selNth", stp='mel',
                     c='polySelectEdgesEveryN "edgeRing" 2;')
    cmds.button(label="Select Nth Edge", w=bw, h=bh, command=polysel_every_n)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=maya_column)
    cmds.shelfButton(i="commandButton.png", w=ic, h=ic, iol="mirCut", stp='mel',
                     c='polyMirrorCut 1 1 0.001;')
    cmds.button(label="polyMirrorCut", w=bw, h=bh, command=polymirrorcut)
    cmds.setParent('..')
    cmds.setParent('..')
#######################################################################

    cmds.tabLayout(tabs, edit=True, tabLabel=((main_column, 'Custom'),(maya_column, 'Maya')))
#######################################################################

if __name__ == '__main__':
    print "modern"
    assetToolsGUI()
