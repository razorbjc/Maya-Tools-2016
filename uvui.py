#!/usr/bin/env python2.7

"""
A custom UV toolset that allows access to the most commonly used tools

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import math


class uvui(object):
    windowName = "UVUI_window"
    def __int__(self):
        self.scale_ratio = 0

    def launch(self):
        # checks if window is already open, closes and recreates if it is
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName, title="UV UI", minimizeButton=False,
                    maximizeButton=False, sizeable=True, rtf=True)
        self.buildui()
        cmds.showWindow()

    # builds layout and buttons, hooks up to commands
    def buildui(self):
        columnmain = cmds.columnLayout(columnWidth=200)
        widthb = 61
        widtha = 40
        widthc = 29
        widthe = 124
        self.scale_ratio = 0

        white = [1, 1, 1]
        red = [.9, .45, .45]
        blue = [.5, .75, .9]
        green = [.45, .8, .45]
        yellow = [.95, .85, .5]
        orange = [.9, .6, .2]
        purple = [.65, .5, .85]

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnmain)
        cmds.button(label="Rot. L", width=widtha, bgc=white, command=self.rotate_left)
        cmds.button(label="Orient", width=widtha, bgc=red, command=self.orient_shells)
        cmds.button(label="Rot. R", width=widtha, bgc=white, command=self.rotate_right)
        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnmain)
        cmds.button(label="Flip U", width=widthb, bgc=blue, command=self.udim_flip_u)
        cmds.button(label="Flip V", width=widthb, bgc=blue, command=self.udim_flip_v)

        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=5)

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnmain)
        cmds.text(label="", width=widtha)
        cmds.button(label="/\\", width=widtha, bgc=white, command=self.translate_up)
        cmds.text(label="", width=widtha)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="<", width=40, bgc=white, command=self.translate_left)
        self.transDistance = cmds.floatField(ed=True, v=1.0, precision=2, s=.25, w=40)
        cmds.button(label=">", width=40, bgc=white, command=self.translate_right)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.text(label="", width=40)
        cmds.button(label="V", width=40, bgc=white, command=self.translate_down)
        cmds.text(label="", width=40)
        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=5)

        # arrows button ends, Layout buttons begin
        ###############################################################
        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Center", width=widthb, bgc=green, command=self.udim_center)
        cmds.button(label="Maximize", width=widthb, bgc=green, command=self.udim_max)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Get TD", width=widthb, bgc=yellow, command=self.get_td)
        cmds.button(label="Set TD", width=widthb, bgc=yellow, command=self.set_td)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="Stack", width=widthb, bgc=purple, command=self.stack_shells)
        cmds.button(label="U", width=widthc, bgc=purple, command=self.distribute_u)
        cmds.button(label="V", width=widthc, bgc=purple, command=self.distribute_v)

        cmds.rowLayout(numberOfColumns=1, p=columnmain)
        cmds.button(label="Layout", width=widthe, bgc=white,
                    command=self.layout)
        cmds.rowColumnLayout(numberOfColumns=2, p=columnmain)
        self.layoutScaleBox = cmds.checkBox(label="Scale", value=True)
        self.layoutRotateBox = cmds.checkBox(label="Rotate")

        # Layout button ends, UV edit buttons begin
        ###############################################################
        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=6)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="Unfold", width=widthb, bgc=blue, command=self.unfold_uv)
        cmds.button(label="U", width=widthc, bgc=blue, command=self.unfold_u)
        cmds.button(label="V", width=widthc, bgc=blue, command=self.unfold_v)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Grid", width=widthb, bgc=red, command=self.grid)
        cmds.button(label="Mirror", width=widthb, bgc=green, command=self.mirror)

        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=4)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.text(label="Transfer UVs", width=90, align="left")
        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Topo", width=widthb, bgc=white, command=self.trans_uv_topo,
                    ann="Transfers UVs from the last selected object \
                        to the rest of your selected objects")
        cmds.button(label="World", width=widthb, bgc=white, command=self.trans_uv_world)
        # End
        ###############################################################

    def gather(self, *args):
        start_udim = self.get_udim()
        cmds.polyEditUV(u=-(start_udim[0]), v=-(start_udim[1]))
        self.udim_center()
        self.udim_max()

    def grid(self, *args):
        start_udim = self.get_udim()
        cmds.ConvertSelectionToFaces()
        sel = cmds.ls(sl=True)
        cmds.ConvertSelectionToUVs()
        mel.eval('polySelectBorderShell 0;')
        cmds.ShrinkPolygonSelectionRegion()
        if len(cmds.ls(sl=True))==0:
            cmds.error("Shell too simple. Use 'Unfold' instead")
        cmds.ConvertSelectionToEdges()
        cmds.InvertSelection()
        cutedges = cmds.ls(sl=True)
        cmds.polyForceUV(sel, uni=True)
        cmds.select(cutedges)
        cmds.InvertSelection()
        cmds.polyMapSewMove(cmds.ls(sl=True), nf=10, lps=0, ch=1)
        cmds.select(sel)
        mel.eval('polySelectBorderShell 0;')
        self.udim_center()
        self.udim_max()
        end_udim = self.get_udim()
        cmds.polyEditUV(u=(start_udim[0]-end_udim[0]), v=(start_udim[1]-end_udim[1]))
        cmds.select(cmds.ls(sl=True), r=True)

    def rotate_left(self, *args):
        center = self.get_center()
        cmds.polyEditUV(pivotU=center[0], pivotV=center[1], angle=45)

    def rotate_right(self, *args):
        center = self.get_center()
        cmds.polyEditUV(pivotU=center[0], pivotV=center[1], angle=-45)

    def translate_up(self, *args):
        cmds.polyEditUV(u=0, v=cmds.floatField(self.transDistance, q=True, v=True))
        cmds.select(cmds.ls(sl=True), r=True)

    def translate_right(self, *args):
        cmds.polyEditUV(u=cmds.floatField(self.transDistance, q=True, v=True), v=0)
        cmds.select(cmds.ls(sl=True), r=True)

    def translate_left(self, *args):
        cmds.polyEditUV(u=-(cmds.floatField(self.transDistance, q=True, v=True)), v=0)
        cmds.select(cmds.ls(sl=True), r=True)

    def translate_down(self, *args):
        cmds.polyEditUV(u=0, v=-(cmds.floatField(self.transDistance, q=True, v=True)))
        cmds.select(cmds.ls(sl=True), r=True)

    def stack_shells(self, *args):
        sel = cmds.ls(sl=True)
        start_pos = self.get_center()
        shells = self.get_shell_array()
        target = self.get_center()
        for i in shells:
            cmds.select(i)
            shell_pos = self.get_center()
            cmds.polyEditUV(u=(target[0]-shell_pos[0]), v=(target[1]-shell_pos[1]))
        cmds.select(sel)
        end_pos = self.get_center()
        cmds.polyEditUV(u=(start_pos[0]-end_pos[0]), v=start_pos[1]-end_pos[1])
        cmds.select(sel)

    def orient_shells(self, *args):
        sel = cmds.ls(sl=True)
        shells = self.get_shell_array()
        for i in shells:
            cmds.select(i)
            self.orient_shell(range=90.0, steps=10.0)
            self.orient_shell(range=10.0, steps=10.0)
            self.orient_shell(range=2.0, steps=15.0)
        cmds.select(sel)

    def get_td(self, *args):
        self.scale_ratio = self.get_scale_ratio()
        print "scale_ratio is", self.scale_ratio

    def set_td(self, *args):
        sel = cmds.ls(sl=True)
        shellarray = self.get_shell_array()

        # iterate through shells and scale by their scale ratios
        for i in shellarray:
            cmds.select(i)
            targetratio = self.get_scale_ratio()
            factor = self.scale_ratio/targetratio
            center = self.get_center()
            cmds.polyEditUV(cmds.ls(sl=True), pu=center[0], pv=center[1], su=factor, sv=factor)
        cmds.select(sel)

    def get_scale_ratio(self, *args):
        # grow to shell and shrink selection to grab internal UVs
        init_sel = cmds.ls(sl=True, fl=True)
        cmds.ConvertSelectionToUVs()
        mel.eval('polySelectBorderShell 0;')
        sel = cmds.ls(sl=True, fl=True)
        cmds.ShrinkPolygonSelectionRegion()
        internal_uvs = cmds.ls(sl=True, fl=True)

        # if no internal edges, then use initial selection
        if len(internal_uvs) == 0:
            internal_uvs = sel
            cmds.select(internal_uvs)
        hero_edge = cmds.polyListComponentConversion(internal_uvs[0], fuv=True, te=True)
        hero_edge = cmds.ls(hero_edge, fl=True, l=True)[0]

        # get world space length of 'hero edge'
        edge_info = cmds.xform(hero_edge, q=True, t=True, ws=True)
        polyedge_length = math.sqrt(math.pow(edge_info[0]-edge_info[3], 2) + math.pow(edge_info[1] - edge_info[4], 2) + math.pow(edge_info[2]-edge_info[5], 2))

        # now convert edge to UVs to get UV length/distance
        herouvs = cmds.polyListComponentConversion(hero_edge, fe=True, tuv=True)
        herouvs = cmds.ls(herouvs, fl=True, l=True)
        herouv_a = cmds.polyEditUVShell(herouvs[0], q=True)
        herouv_b = cmds.polyEditUVShell(herouvs[1], q=True)
        uvedge_length = math.sqrt(math.pow(herouv_a[0] - herouv_b[0], 2) + math.pow(herouv_a[1] - herouv_b[1], 2))

        # find ratio between UV length and worldspace edge length
        ratio = uvedge_length/polyedge_length
        cmds.select(init_sel)
        return ratio

    def udim_flip_u(self, *args):
        udim = self.get_udim()
        tilecenter = udim[0] + .5
        cmds.polyEditUV(pivotU=tilecenter, scaleU=-1)
        cmds.select(cmds.ls(sl=True), r=True)

    def udim_flip_v(self, *args):
        udim = self.get_udim()
        tilecenter = udim[1] + .5
        cmds.polyEditUV(pivotV=tilecenter, scaleV=-1)
        cmds.select(cmds.ls(sl=True), r=True)

    def udim_center(self, *args):
        center = self.get_center()
        udim = self.get_udim()
        utarget = udim[0] + .5  # find center of udim
        vtarget = udim[1] + .5
        cmds.polyEditUV(u=(utarget-center[0]), v=(vtarget-center[1]))
        cmds.select(cmds.ls(sl=True), r=True)

    def udim_max(self, *args):
        center = self.get_center()
        uminmax, vminmax, = cmds.polyEvaluate(bc2=True)
        width = math.fabs(uminmax[0] - uminmax[1])
        height = math.fabs(vminmax[0] - vminmax[1])
        if width > height:
            factor = .98/width
        else:
            factor = .98/height
        cmds.polyEditUV(pivotU=center[0], pivotV=center[1],
                        scaleV=factor, scaleU=factor)
        cmds.select(cmds.ls(sl=True), r=True)

    def layout(self, *args):
        scale_on = cmds.checkBox(self.layoutScaleBox, q=True, value=True)
        rotate_on = cmds.checkBox(self.layoutRotateBox, q=True, value=True)
        start_udim = self.get_udim()
        if scale_on and rotate_on:
            cmds.polyMultiLayoutUV(lm=1, l=2, sc=1, psc=2, rbf=1, fr=1, ps=.5)

        elif scale_on and not rotate_on:
            cmds.polyMultiLayoutUV(lm=1, l=2, sc=1, psc=2, rbf=0, fr=1, ps=.5)

        elif rotate_on and not scale_on:
            cmds.polyMultiLayoutUV(lm=1, l=2, sc=1, psc=0, rbf=1, fr=1, ps=.5)

        else:
            cmds.polyMultiLayoutUV(lm=1, l=2, sc=1, psc=0, rbf=0, fr=1, ps=.5)

        cmds.polyEditUV(u=start_udim[0], v=start_udim[1])

    def unfold_uv(self, *args):
        cmds.Unfold3D(cmds.ls(sl=True), u=1, ite=1, p=0, bi=1, tf=1, ms=1024, rs=2)

    def unfold_u(self, *args):
        cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=2, us=False)

    def unfold_v(self, *args):
        cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=1, us=False)

    def trans_uv_topo(self, *args):
        selection = cmds.ls(sl=True, o=True)
        reference = selection[0]
        selection.remove(reference)
        for i in selection:
            cmds.transferAttributes(reference, i,
                                    transferNormals=0,
                                    transferUVs=2,
                                    sampleSpace=5,
                                    searchMethod=0)
            cmds.delete(i, ch=True)

    def trans_uv_world(self, *args):
        selection = cmds.ls(sl=True, o=True)
        reference = selection[0]
        selection.remove(reference)
        for i in selection:
            cmds.transferAttributes(reference, i,
                                    transferPositions=0,
                                    transferNormals=0,
                                    transferUVs=2,
                                    sourceUvSpace="map1",
                                    targetUvSpace="map1",
                                    sampleSpace=0,
                                    searchMethod=0)
            cmds.delete(i, ch=True)

    def distribute_v(self, *args):
        startcenter = self.get_center()
        sel = cmds.ls(sl=True)
        target = self.get_center()
        shells = self.get_shell_array()
        spacing = 0
        for i in shells:
            cmds.select(i)
            shell_pos = self.get_center()
            bbox = cmds.polyEvaluate(boundingBoxComponent2d=True)
            v_spacing = (bbox[1][1]-bbox[1][0])/2
            spacing = spacing + v_spacing
            cmds.polyEditUV(u=target[0]-shell_pos[0], v=(target[1]+spacing)-shell_pos[1])
            spacing = spacing + v_spacing + .007
        cmds.select(sel)
        end_center = self.get_center()
        cmds.polyEditUV(u=(startcenter[0]-end_center[0]),
                        v=(startcenter[1]-end_center[1]))
        cmds.select(cmds.ls(sl=True), r=True)

    def distribute_u(self, *args):
        startcenter = self.get_center()
        sel = cmds.ls(sl=True)
        target = self.get_center()
        shells = self.get_shell_array()
        spacing = 0
        for i in shells:
            cmds.select(i)
            shell_pos = self.get_center()
            bbox = cmds.polyEvaluate(boundingBoxComponent2d=True)
            u_spacing = (bbox[0][1]-bbox[0][0])/2
            spacing = spacing + u_spacing
            cmds.polyEditUV(u=(target[0]+spacing)-shell_pos[0], v=(target[1]-shell_pos[1]))
            spacing = spacing + u_spacing + .007
        cmds.select(sel)
        end_center = self.get_center()
        cmds.polyEditUV(u=(startcenter[0]-end_center[0]),
                        v=(startcenter[1]-end_center[1]))
        cmds.select(cmds.ls(sl=True), r=True)

    def autoseams(self, *args):
        mel.eval('performPolyAutoSeamUV 0;')

    def get_udim(self):
        # tuple of two pairs in Python: ((xmin,xmax), (ymin,ymax))
        maxmin = cmds.polyEvaluate(bc2=True)
        u_avg = (maxmin[0][0] + maxmin[0][1])/2
        v_avg = (maxmin[1][0] + maxmin[1][1])/2
        u_tile = math.floor(u_avg)
        v_tile = math.floor(v_avg)
        udim_tuple = (u_tile, v_tile)
        return udim_tuple

    def get_center(self):
        # tuple of two pairs in Python: ((xmin,xmax), (ymin,ymax))
        maxmin = cmds.polyEvaluate(bc2=True)
        u_avg = (maxmin[0][0] + maxmin[0][1])/2
        v_avg = (maxmin[1][0] + maxmin[1][1])/2
        center_tuple = (u_avg, v_avg)
        return center_tuple

    def mirror(self, *args):
        cmds.ConvertSelectionToContainedFaces()
        selection = cmds.ls(sl=True)  # starting UVs
        objs = cmds.ls(sl=True, o=True)
        cmds.ConvertSelectionToContainedEdges()
        cmds.select(selection)
        mel.eval('textureWindowSelectConvert 4;')
        mel.eval('polySelectBorderShell 1;')
        cmds.ConvertSelectionToContainedEdges()
        shelledges = cmds.ls(sl=True, flatten=True)  # get border edge of UV shell

        cmds.select(selection)  # get selected faces
        mel.eval('PolySelectTraverse 1;')  # grow face selection
        cmds.ConvertSelectionToEdgePerimeter()  # grab selection perimeter
        # get border edge of user selection
        sel_perimeter = cmds.ls(sl=True, flatten=True)

        # get list of edges to sew, selection border edge that is NOT a shell edge
        sew_edges = [i for i in sel_perimeter if i not in shelledges]

        cmds.select(selection)  # select faces to run transfer Attributes
        mel.eval('textureWindowSelectConvert 4;')  # convert selection to UVs
        mel.eval('PolySelectTraverse 1;')  # grow selection without crossing UV borders
        cmds.ConvertSelectionToContainedFaces()

        start_udim = self.get_udim()
        cmds.transferAttributes(transferPositions=0,
                                transferNormals=0,
                                transferUVs=2,
                                transferColors=0,
                                sampleSpace=0,
                                searchMethod=0,
                                searchScaleX=-1.0,
                                flipUVs=1,
                                colorBorders=1)
        end_udim = self.get_udim()

        # clean history and move back to original UDIM, sew edges
        cmds.delete(objs[0], ch=True)
        cmds.polyEditUV(u=(start_udim[0]-end_udim[0]), v=0)
        for i in sew_edges:
            cmds.polyMapSew(i)
        cmds.select(selection)
        mel.eval('BakeNonDefHistory;')

    def get_sumdif(self, *args):
        bbox = cmds.polyEvaluate(boundingBoxComponent2d=True)
        return (bbox[0][1]-bbox[0][0]) + (bbox[1][1]-bbox[1][0])

    def orient_shell(self, range=90.0, steps=90.0):
        start_pos = self.get_center()
        bbox = cmds.polyEvaluate(boundingBoxComponent2d=True)
        pivotu = (bbox[0][1]-bbox[0][0])/2
        pivotv = (bbox[1][1]-bbox[1][0])/2
        increment = range/steps
        i = 0
        bestscore = 100
        bestangle = 0
        cmds.polyEditUV(pivotU=(bbox[0][1]-bbox[0][0])/2, pivotV=(bbox[1][1]-bbox[1][0])/2, angle=-range/2)
        while i < steps:
            score = self.get_sumdif()
            if score < bestscore:
                bestscore = score
                bestangle = i*increment
            i = i+1
            cmds.polyEditUV(pivotU=pivotu, pivotV=pivotv, angle=increment)
        cmds.polyEditUV(pivotU=pivotu, pivotV=pivotv, angle=-range)
        cmds.polyEditUV(pivotU=pivotu, pivotV=pivotv, angle=bestangle)
        end_pos = self.get_center()
        cmds.polyEditUV(u=(start_pos[0]-end_pos[0]), v=(start_pos[1]-end_pos[1]))
        cmds.select(cmds.ls(sl=True), r=True)

    def get_shell_array(self, *args):
        shell_array = []
        cmds.ConvertSelectionToUVs()
        sel = set()
        sel.update(cmds.ls(sl=True, fl=True))
        while sel:
            example = sel.pop()
            cmds.select(example)
            mel.eval('polySelectBorderShell 0;')
            current_shell = cmds.ls(sl=True, fl=True)
            shell_array.append(current_shell)
            for j in current_shell:
                if j in sel:
                    sel.remove(j)
        return shell_array
