import hou

def add_nodes(bundle,sel_nodes,set_color):
    for node in sel_nodes:
        bundle.addNode(node)
        node.setColor(set_color)

# Here we are creating a function which when on alt-clicking
# will remove the selected nodes from the bundle.
def setup_bundle(kwargs):
    set_color = hou.Color(0.1,0.1,0.1)
    default_color = hou.Color(0.8,0.8,0.8)
    sel_nodes = hou.selectedNodes()
    bundle = hou.nodeBundle("myBundle1")
    if bundle:
        if kwargs["altclick"] and not kwargs["ctrlclick"]:
            if sel_nodes:
                for nodes in sel_nodes:
                    bundle.removeNode(nodes)
        elif kwargs["altclick"] and kwargs["ctrlclick"]:
            created_nodes = bundle.nodes()
            bundle.destroy()
            for node in created_nodes:
                node.setColor(default_color)
                
        elif sel_nodes:
            add_nodes(bundle,sel_nodes,set_color)
    else:
        bundle = hou.addNodeBundle("myBundle1")
        if sel_nodes:
            add_nodes(bundle,sel_nodes,set_color)
    
setup_bundle(kwargs)