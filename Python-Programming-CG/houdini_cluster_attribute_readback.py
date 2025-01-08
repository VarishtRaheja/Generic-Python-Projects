#Python script which will read back the cluster attribute - this will also work on other attributes.
#Created by Varisht Raheja
#Version 1 - March, 2020

node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.

file_eval = hou.evalParm("filename") #Create a parameter called filename and store the path in the parameter
with open(file_eval,"r") as file:
    data = file.read()
    for line in data.splitlines():
        if not line:
            continue
            #Creating the points after parsing each x,y,z values in the file.
        line = line[1:-1].split(",")
        x = float(line[0])
        y = float(line[1])
        z = float(line[2])
        
        #Function inside houdini to generate points based on positional values.
        finalPos = geo.createPoint()
        finalPos.setPosition((x,y,z))
