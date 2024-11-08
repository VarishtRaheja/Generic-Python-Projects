#Python Script to write out the cluster attribute inside Houdini.
#Created by Varisht Raheja - Version 1 - March, 2020

node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.

read = hou.ch('output')
values = geo.pointIntAttribValues("cluster") #save attribute values of each cluster
#Choice of saving it as a csv or txt depedning on user

for i in list(set(values)):
    if read == 0:
        myTxt = file("D:Thesis/Terrain_Application/Data/data_"+str(i)+".txt","w")
    elif read == 1:
        myTxt = file("D:Thesis/Terrain_Application/Data/data_"+str(i)+".csv","w")
        
        #Writng out the point position of each cluster.
        
    for points in zip(values,geo.points()):
        if points[0] == i:
            pos = points[1].position()
            pos = str(pos) + "\n"
            myTxt.write(pos)
myTxt.close()
