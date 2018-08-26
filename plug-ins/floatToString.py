"""			
This plugin will register a Maya node that can convert a float to a string so 
it can be used in combination with an annotation. The display precision can 
be adjusted and so can a prefix and suffix be added.

.. figure:: /_images/floatToString.png
   :align: center

Installation
============
* Extract the content of the .rar file anywhere on disk.
* Drag the floatToString.mel file in Maya to permanently install the plugin.

Usage
=====
Node
::
    from maya import cmds

    # create nodes
    floatToString = cmds.createNode("floatToString")
    annotation = cmds.createNode("annotationShape")

    # set attributes
    cmds.setAttr("{0}.precision".format(floatToString), 1)
    cmds.setAttr("{0}.prefix".format(floatToString), "height:", type="string")
    cmds.setAttr("{0}.suffix".format(floatToString), "mm", type="string")

    # connect to annotation
    cmds.connectAttr(
        "{0}.output".format(floatToString),
        "{0}.text".format(annotation)
    )
"""
from maya import OpenMaya, OpenMayaMPx

__author__ = "Robert Joosten"
__version__ = "0.1.1"
__email__ = "rwm.joosten@gmail.com"


class FloatToStringNode(OpenMayaMPx.MPxNode):
    kPluginNodeName = "floatToString"
    kPluginNodeId = OpenMaya.MTypeId(0x31550)
    kPluginNodeClassify = "utility/general"

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        # get input
        floatData = data.inputValue(self.float)
        floatValue = floatData.asFloat()

        precisionData = data.inputValue(self.precision)
        precisionValue = precisionData.asInt()

        prefixData = data.inputValue(self.prefix)
        prefixValue = prefixData.asString()

        suffixData = data.inputValue(self.suffix)
        suffixValue = suffixData.asString()

        # set output
        outputVolume = data.outputValue(self.output)
        outputVolume.setString(
            "{p} {n:.{d}f} {s}".format(
                n=floatValue,
                d=precisionValue,
                p=prefixValue,
                s=suffixValue
            ).strip()
        )

        data.setClean(plug)

    @classmethod
    def nodeCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())

    @classmethod
    def nodeInitializer(cls):
        # float input
        floatAttr = OpenMaya.MFnNumericAttribute()
        cls.float = floatAttr.create(
            "float",
            "f",
            OpenMaya.MFnNumericData.kFloat,
            0.0
        )
        floatAttr.setKeyable(True)

        # precision input
        precisionAttr = OpenMaya.MFnNumericAttribute()
        cls.precision = precisionAttr.create(
            "precision",
            "prec",
            OpenMaya.MFnNumericData.kInt,
            3
        )
        precisionAttr.setKeyable(True)

        # prefix input
        stringData = OpenMaya.MFnStringData().create("")
        prefixAttr = OpenMaya.MFnTypedAttribute()
        cls.prefix = prefixAttr.create(
            "prefix",
            "pref",
            OpenMaya.MFnData.kString,
            stringData
        )

        # suffix input
        stringData = OpenMaya.MFnStringData().create("")
        suffixAttr = OpenMaya.MFnTypedAttribute()
        cls.suffix = suffixAttr.create(
            "suffix",
            "suf",
            OpenMaya.MFnData.kString,
            stringData
        )

        # output
        stringData = OpenMaya.MFnStringData().create("")
        outputAttr = OpenMaya.MFnTypedAttribute()
        cls.output = outputAttr.create(
            "output",
            "o",
            OpenMaya.MFnData.kString,
            stringData
        )
        outputAttr.setWritable(False)

        # add attributes
        cls.addAttribute(cls.float)
        cls.addAttribute(cls.precision)
        cls.addAttribute(cls.prefix)
        cls.addAttribute(cls.suffix)
        cls.addAttribute(cls.output)

        # add dependencies
        cls.attributeAffects(cls.float, cls.output)
        cls.attributeAffects(cls.precision, cls.output)
        cls.attributeAffects(cls.prefix, cls.output)
        cls.attributeAffects(cls.suffix, cls.output)


# ----------------------------------------------------------------------------


def initializePlugin(mObject):
    mPlugin = OpenMayaMPx.MFnPlugin(mObject)
    try:
        mPlugin.registerNode(
            FloatToStringNode.kPluginNodeName,
            FloatToStringNode.kPluginNodeId,
            FloatToStringNode.nodeCreator,
            FloatToStringNode.nodeInitializer
        )
    except:
        raise RuntimeError(
            "Failed to register : {0}".format(
                FloatToStringNode.kPluginNodeName
            )
        )


def uninitializePlugin(mObject):
    mPlugin = OpenMayaMPx.MFnPlugin(mObject)
    try:
        mPlugin.deregisterNode(
            FloatToStringNode.kPluginNodeId
        )
    except:
        raise RuntimeError(
            "Failed to deregister : {0}".format(
                FloatToStringNode.kPluginNodeName
            )
        )


# ----------------------------------------------------------------------------


AETemplateCommand = """
global proc AEfloatToStringTemplate( string $nodeName )
{
    editorTemplate -beginScrollLayout;

    editorTemplate -beginLayout "Input" -collapse 0;
        editorTemplate -addControl "float";
        editorTemplate -addControl "precision";
        editorTemplate -addControl "prefix";
        editorTemplate -addControl "suffix";
    editorTemplate -beginLayout "Output" -collapse 0;
        editorTemplate -addControl "output";

    editorTemplate -endLayout;

    AEdependNodeTemplate $nodeName;

    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}
"""
OpenMaya.MGlobal.executeCommand(AETemplateCommand, False, False)
