import os, hou

extensions = ["obj","fbx","png","jpg"]

# Creating and checking if "loader" node at geo context exists!
root = hou.node("/obj/")
name = "Loader"

# Function creation

def create_geo(node_name):
    if hou.node("{}/{}".format(root,node_name))==None:
        obj_loader = root.createNode("geo",node_name)
        hou.ui.displayMessage('{} node created!'.format(node_name))
        return obj_loader
    else:
        for nodes in root.children():
            nodes.destroy()
        hou.ui.displayMessage("Obj level cleared.")
    
# Calling the function
obj_loader = create_geo(name)

# Grabbing files from a directory 
dir = hou.ui.selectFile(title="Selet a directory",file_type=hou.fileType.Directory)
expand_dir = hou.expandString(dir)
obj_list_dir = os.listdir(expand_dir)
merge = obj_loader.createNode("merge","merge_objs",run_init_scripts=False)

# Grabbing all the files in the user selected folder
for index, obj_files in enumerate(obj_list_dir):
    path = os.path.abspath(os.path.join(expand_dir+"/",obj_files))
    elems = obj_files.rsplit(".")
    ext = elems[-1].lower()
    file_name = elems[0].lower()
    if ext in extensions:
        file_node = obj_loader.createNode("file",file_name)
        file_node.parm("file").set(path)
        merge.setInput(index,file_node)

# Settting up the nodes to display
obj_loader.layoutChildren()
merge.setDisplayFlag(True)
merge.setRenderFlag(True)