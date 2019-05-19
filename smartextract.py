#!/usr/bin/env python2.7

"""
Works with Maya 2016
meant to replace Maya's extract
if objects with separate meshes are selected, smartExtract will separate them

if given a face selection, smartExtract will extract faces but retain the name and pivot
of the base geometry. The extracted pieces will be named/numbered and pivots centered

if given an completed edge loop, smartExtract will run faceCut and then extract faces

if given vertices, the vertex selection will be converted to a face select and extract

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import jc_facecut


def smartextract():
	sel = cmds.ls(sl=True)
	print "selection check:", sel
	# object selected: run separate
	if cmds.nodeType(sel[0]) == 'transform':

		for obj in sel:
			parents = cmds.listRelatives(obj, parent=True, fullPath=True)
			result_list = []
			name = obj
			separate_obj = cmds.polySeparate(obj, ch=False)
			first = [separate_obj.pop(0)]
			result_list.extend(rebuild(separate_obj, "separate", parents))
			main_obj = rebuild(first, name, parents, primary=True)[0]
			cmds.delete(obj)
			main_obj = cmds.rename(main_obj, name)
			print "adding:", main_obj
			result_list.append(main_obj)

		cmds.select(result_list)
		return True

	if cmds.nodeType(sel[0]) != 'mesh':
		return False

	# get transform name, parents/hierachy
	name = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True, fullPath=True)[0]
	parents = cmds.listRelatives(name, parent=True, fullPath=True)

	# Run face extraction, then pop off the Separate node, and remove original geo
	tofaces(sel)
	cmds.polyChipOff(ch=1, kft=1, dup=0)
	obj=cmds.ls(sl=True, o=True)
	cmds.polySeparate(obj, rs=1, ch=1)
	extracted = cmds.ls(sl=True, o=True)
	if len(extracted) < 2:
		cmds.error("Must select a completed edge loop")
		return False

	original = [getbiggest(extracted)]
	extracted.remove(original[0])  # remove the biggest piece, which will keep original name

	# Restore hierarchy, center piv, rename, del history
	cmds.rename(cmds.listRelatives(original[0], p=True, fullPath=True)[0], "xxx")
	new_original = rebuild(original, name.split("|")[-1], parents, True)
	new_extracted = rebuild(extracted, "extract", parents)
	cmds.select(new_original, r=True)
	cmds.select(new_extracted, add=True)
	cmds.select(cmds.ls(sl=True, o=True))
	return True


def smartduplicate():
	sel = cmds.ls(sl=True)

	# object selected: run separate
	if cmds.nodeType(sel[0]) == 'transform':
		mel.eval('Duplicate;')
		return True

	if cmds.nodeType(sel[0]) != 'mesh':
		return True

	# get transform name, parents/hierachy
	name = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True, fullPath=True)[0]
	parents = cmds.listRelatives(name, parent=True, fullPath=True)
	pivotinfo = cmds.xform(name, q=True, pivots=True, ws=True)[:3]

	tofaces(sel)
	cmds.polyChipOff(ch=1, kft=1, dup=1)
	obj=cmds.ls(sl=True, o=True)
	cmds.polySeparate(obj, rs=1, ch=1)
	duplicated = cmds.ls(sl=True, o=True)
	if len(duplicated) < 2:
		cmds.error("Must select a completed edge loop")
		return False

	original = [getbiggest(duplicated)]
	duplicated.remove(original[0])

	# Restore hierarchy, center piv, rename, del history
	cmds.rename(cmds.listRelatives(original[0], p=True, fullPath=True)[0], "xxx")
	rebuild(
		array=original,
		name=name.split("|")[-1],
		group=parents,
		primary=True,
		freeze=False,
		pivot=pivotinfo)
	new_duplicated = rebuild(array=duplicated, name="duplicate", group=parents)
	print "duplicated:", new_duplicated
	cmds.select(new_duplicated)
	cmds.select(cmds.ls(sl=True, o=True))
	return True


def rebuild(array=None, name=None, group=None, primary=False, freeze=True, pivot=None):
	finalarray = []
	count = 1001
	print "first gets array:", array
	for i in array:
		newname = cmds.parent(i, group) if group else cmds.parent(i, world=True)
		if freeze:
			cmds.makeIdentity(newname, apply=True, r=True, s=True, t=True)
		if pivot:
			cmds.xform(newname, pivots=pivot, ws=True)
		else:
			cmds.xform(newname, cp=True)
		cmds.delete(newname, ch=True)
		final = cmds.rename(newname, name) if primary else cmds.rename(newname, name + "_%0*d" % (4, count))
		finalarray.append(final)
		count += 1
	return finalarray


def getbiggest(array=None):
	biggestvol = 0
	biggestitem = None
	for i in array:
		bbox = cmds.exactWorldBoundingBox(i)
		dimensions = [bbox[3] - bbox[0], bbox[4] - bbox[1], bbox[5] - bbox[2]]
		volume = dimensions[0] * dimensions[1] * dimensions[2]
		if volume > biggestvol:
			biggestvol = volume
			biggestitem = i
	return biggestitem


def tofaces(sel):
	# checks for edge selection(mask 32) & vertices(mask 31), then converts them to faces
	if cmds.filterExpand(sel[0], selectionMask=31):
		cmds.ConvertSelectionToContainedFaces()
	if cmds.filterExpand(sel[0], selectionMask=32):
		jc_facecut.facecut()
	cmds.ConvertSelectionToFaces()
	return True
