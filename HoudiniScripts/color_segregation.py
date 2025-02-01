import hou
import random,colorsys

scene_root = hou.node("/obj/")
geo_node_name = "color_segregation"
if hou.node("/obj/{}".format(geo_node_name))==None:
    geo_node = scene_root.createNode("geo",run_init_scripts=False)
    geo_node.setName(geo_node_name)
    if geo_node.numItems() == 0:
        crag = geo_node.createNode("testgeometry_crag",run_init_scripts=False)
        unpack = geo_node.createNode("unpack",run_init_scripts=False)
        unpack.setFirstInput(crag,0)
        unpack.moveToGoodPosition(True)
        
        # Creating connectivity node for "class" attrib
        connect = geo_node.createNode("connectivity",run_init_scripts=False)
        connect.setNextInput(unpack)
        connect.moveToGoodPosition(True)
        connect.setSelected(True)
        
        # Creating a parent path to drop nodes into context.
        connect_sel_node = hou.selectedNodes()[0]
        parent = connect_sel_node.parent()
        connect_sel_node.parm("connecttype").set(1)
        attrib = connect_sel_node.evalParm("attribname")
        
        # Grabbing geo level attributes
        geo = connect_sel_node.geometry()
        class_value = set([pr.attribValue(attrib) for pr in geo.prims()])

        # Creating a merge node
        merge_node = parent.createNode("merge")
        
        for value in class_value:
            blast = hou.Node.path(connect_sel_node.createOutputNode("blast"))
            blast = hou.node(blast)
            blast.parm("group").set("@"+attrib+"="+str(value))
            blast.parm("negate").set(1)
            rgb_color = colorsys.hsv_to_rgb(random.random(),random.random(),random.random())
            color = hou.Color((rgb_color))
            color_node = hou.node(hou.Node.path(blast.createOutputNode("color")))
            color_node.parmTuple("color").set((rgb_color[0],rgb_color[1],rgb_color[2]))
            merge_node.setNextInput(color_node)
            merge_node.moveToGoodPosition(True)
            merge_node.setSelected(True)

        parent.layoutChildren() 
        connect.setSelected(False)
        merge_node.setDisplayFlag(True)
        merge_node.setRenderFlag(True)

else:
    hou.ui.displayMessage("Geo node exists!")
    

