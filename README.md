# rjFloatToString
<img align="right" src="https://github.com/robertjoosten/rjFloatToString/blob/master/icons/floatToString.png">
This plugin will register a Maya node that can convert a float to a string so it can be used in combination with an annotation. The display precision can be adjusted and so can a prefix and suffix be added.

## Installation
Copy the **rjFloatToString.py** file in any of the directories that are in your MAYA_PLUG_IN_PATH environment variable:
> C:\Program Files\Autodesk\<MAYA_VERSION>\plug-ins

Copy all the png files in any of the directories that are in your XBMLANGPATH environment variable:
> C:\Program Files\Autodesk\<MAYA_VERSION>\icons

## Usage     
**Node:**
```python
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
```
        
        
