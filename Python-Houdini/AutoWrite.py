import nuke


def autoWrite():

    currentNode = nuke.createNode('Write',inpanel = False)
    currentNode.knob("name").setValue("AutoWrite")

    selNode = nuke.root().name()
    if selNode != "Root":
        splitPath = selNode.split('/')[:-1]
        splitPath = ('/').join(splitPath)

        custom = nuke.Tab_Knob('Tab Fragments')
        currentNode.addKnob(custom)
        currentNode.addKnob(nuke.EvalString_Knob('script', 'Script Name','[file rootname [file tail [value root.name] ] ]'))
        feedback = """
        [value file]
        [value this.input.name]
    
    
    
    """
        currentNode.knob('label').setValue(feedback)

        OutputFile = splitPath+".%04d."+nuke.getInput("data Type")
        newFile = OutputFile.split('/')[-1:]
        newFile = newFile[0].split('.')[-1]
    

        currentNode['file'].setValue(OutputFile)
        currentNode['file_type'].setValue(newFile)
        s = nuke.ask("Shall i execute?")
        if s == True:
            nuke.execute(currentNode,start = 1, end = int(nuke.getInput("Enter Last Frame")))
    
        
    else:
        nuke.message("Please save the file")

autoWrite()

