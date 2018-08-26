# maya-plugin-float-to-string
<p align="center"><img src="icons/floatToString.png?raw=true"></p>
This plugin will register a Maya node that can convert a float to a string so it can be used in combination with an annotation. The display precision can be adjusted and so can a prefix and suffix be added.

## Installation
* Extract the content of the .rar file anywhere on disk.
* Drag the floatToString.mel file in Maya to permanently install the plugin.

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
        
        
