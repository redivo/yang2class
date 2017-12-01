#!/usr/bin/python
import xml.etree.ElementTree as ET

tree = ET.parse('yang.xml')
root = tree.getroot()

# Node types
NODE_TYPE_MODULE    = 'module'
NODE_TYPE_LEAF      = 'leaf'
NODE_TYPE_CONTAINER = 'container'
NODE_TYPE_AUGMENT   = 'augment'
NODE_TYPE_LIST      = 'list'
NODE_TYPE_LEAFLIST  = 'leaf-list'
NODE_TYPE_USES      = 'uses'

####################################################################################################

class Module:
    def __init__(self, name, path="/", valueType=""):
        self.name = name
        self.nodeType = NODE_TYPE_MODULE
        self.children = []

    def addChildNode(self, child):
        self.children.append(child)

    def showRecursive(self, prePrintLine = ""):
        print prePrintLine + "Module " + self.name
        for child in self.children:
            child.showRecursive(prePrintLine + "|   ")
        print prePrintLine + "'"

class Leaf:
    def __init__(self, name, path, valueType):
        self.name = name
        self.path = path
        self.valueType = valueType
        self.nodeType = NODE_TYPE_MODULE

    def getPath(self):
        return self.path

    def showRecursive(self, prePrintLine = ""):
        print prePrintLine + "Leaf " + self.name
        print prePrintLine + "|   Type: " + self.valueType
        print prePrintLine + "|   Path: " + self.path
        print prePrintLine + "'"

class Container:
    def __init__(self, name, path, valueType=""):
        self.name = name
        self.nodeType = NODE_TYPE_CONTAINER
        self.path = path
        self.children = []

    def getPath(self):
        return self.path

    def addChildNode(self, child):
        self.children.append(child)

    def showRecursive(self, prePrintLine = ""):
        print prePrintLine + "Container " + self.name
        print prePrintLine + "|   Path: " + self.path
        for child in self.children:
            child.showRecursive(prePrintLine + "|   ")
        print prePrintLine + "'"

####################################################################################################

DataNodeTypes = {
    NODE_TYPE_MODULE : Module,
    NODE_TYPE_LEAF : Leaf,
    NODE_TYPE_CONTAINER : Container,
    #'augment' : 0,
    #'list' : 0,
    #'leaf-list' : 0,
    #'uses' : 0,
}

####################################################################################################

def createNode(xmlElem, path):
    tag = xmlElem.tag.split('}')
    tag = tag[len(tag) - 1]

    if not (tag in DataNodeTypes):
        return None

    currentPath = path + xmlElem.attrib["name"] + "/"

    # Get type of leaf
    valueType = ""
    if tag == NODE_TYPE_LEAF:
        for prop in xmlElem:
            propTag = prop.tag.split('}')
            propTag = propTag[len(propTag) - 1]

            if propTag == "type":
                valueType = prop.attrib["name"]
                break

    node = DataNodeTypes[tag](xmlElem.attrib["name"], currentPath, valueType)

    return node

####################################################################################################

def IterateOverNode(parentNode, xmlElem, path = "/"):
    for child in xmlElem:
        node = createNode(child, path)
        if node == None:
            continue

        parentNode.addChildNode(node)
        IterateOverNode(node, child, node.getPath())

####################################################################################################


rootNode = createNode(root, "")
IterateOverNode(rootNode, root)

rootNode.showRecursive()
