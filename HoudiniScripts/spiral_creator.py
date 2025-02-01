import hou

root_scene = hou.node("/obj/")
spiral = root_scene.createNode("geo","spiral")
line = spiral.createNode("line","creating_line")
vex_expression = """float pt01 = float(@ptnum)/@numpt;
@P.x = cos(pt01*chf("freq"))*chf("amp")*chramp("radius",pt01,0);
@P.y = pt01*chf("amp");
@P.z = sin(pt01*chf("freq"))*chf("amp")*chramp("radius",pt01,0);"""

def wrangle_node():
    # Created the line node
    wrangle = line.createOutputNode("attribwrangle","spiral_controls")
    wrangle.setSelected(True)
    
    # Created the null node
    null = wrangle.createOutputNode("null","OUT_SPIRAL_CONTROL")
    
    # Crated spare paramters and default values on the wrangle node.
    npoints = hou.IntParmTemplate("npoints","Number of Points",1,(50,0,0),1,200)
    wrangle.addSpareParmTuple(npoints)
    
    freq = hou.FloatParmTemplate("freq","Frequency",1,(600,0,0),0.0,1000.0)
    wrangle.addSpareParmTuple(freq)
    
    amp = hou.FloatParmTemplate("amp","Amplitude",1,(2,0,0),0.0,4.0)
    wrangle.addSpareParmTuple(amp)
    
    length = hou.FloatParmTemplate("length","Length",1,(3.0,0.0,0.0),0,5)
    wrangle.addSpareParmTuple(length)
    
    rmap = hou.RampParmTemplate("radius","Radius",hou.rampParmType.Float)
    wrangle.addSpareParmTuple(rmap)
    
    wrangle.parm("snippet").set(vex_expression)
    line.parm("points").setExpression("ch('../{}/{}')".format(wrangle.name(),npoints.name()))
    
    
    # returning the null node at the end
    null.setDisplayFlag(True)
    null.setRenderFlag(True)
    return null

wrangle_node()
