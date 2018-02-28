#!/usr/bin/python
import xml.etree.ElementTree as ET
from pprint import pprint

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

YangTypeConversion = {
    'int8'   : 'int8_t',
    'uint8'  : 'uint8_t',
    'int16'  : 'int16_t',
    'uint16' : 'uint16_t',
    'int32'  : 'int32_t',
    'uint32' : 'uint32_t',
    'string' : 'std::string',
}

####################################################################################################

def yangName2ClassName(yangName):
    return yangName.title().replace('-', '').replace('_', '')

def yangName2VarName(yangName):
    return yangName.lower().replace('-', '_') + '_'

class Module:
    def __init__(self, xmlElem, path='/'):
        self.name = xmlElem.attrib['name']
        self.nodeType = NODE_TYPE_MODULE
        self.children = []

    def addChildNode(self, child):
        self.children.append(child)

    def getName(self):
        return self.name

    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Module ' + self.name
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

    def getRecursiveCppHeader(self):
        header = ''

        for child in self.children:
            header += child.getRecursiveCppChildHeader()

        header += 'class ' + yangName2ClassName(self.name) + ' {\n'
        header += '   private:\n'
        for child in self.children:
            header += child.getCppInstantiate('    ')
        header += '};'
        return header

class Leaf:
    def __init__(self, xmlElem, path):
        # Get type of leaf
        valueType = ''
        for prop in xmlElem:
            propTag = prop.tag.split('}')
            propTag = propTag[len(propTag) - 1]

            if propTag == 'type':
                valueType = prop.attrib['name']
                break

        self.name = xmlElem.attrib['name']
        self.path = path
        self.valueType = valueType
        self.nodeType = NODE_TYPE_MODULE

    def getRecursiveCppChildHeader(self):
        return ''

    def getCppInstantiate(self, preIdent = ''):
        return preIdent + 'Leaf<' + YangTypeConversion[self.valueType] + '>' \
                        + ' ' + yangName2VarName(self.name) + ';\n'

    def getType(self):
        return self.valueType

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Leaf ' + self.name
        print prePrintLine + '|   Type: ' + self.valueType
        print prePrintLine + '|   Path: ' + self.path
        print prePrintLine + '\''

class Container:
    def __init__(self, xmlElem, path):
        self.name = xmlElem.attrib['name']
        self.nodeType = NODE_TYPE_CONTAINER
        self.path = path
        self.children = []

    def getRecursiveCppChildHeader(self):
        header = ''

        for child in self.children:
            header += child.getRecursiveCppChildHeader()

        header += 'class ' + yangName2ClassName(self.name) + ' : BasicNode {\n'
        header += '   public:\n'
        header += '    ' + yangName2ClassName(self.name) + ' : BasicNode("' + self.path + '") {}\n'
        header += '\n'
        header += '   private:\n'
        #for child in self.children:
        #    header += child.getCppInstantiate('    ')
        header += '};\n\n'

        return header

    def getCppInstantiate(self, preIdent = ''):
        return preIdent + yangName2ClassName(self.name) + ' ' + yangName2VarName(self.name) + ';\n'

    def getPath(self):
        return self.path

    def addChildNode(self, child):
        self.children.append(child)

    def getName(self):
        return self.name

    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Container ' + self.name
        print prePrintLine + '|   Path: ' + self.path
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

class List:
    def __init__(self, xmlElem, path):
        # Get key
        keyName = ''
        for prop in xmlElem:
            propTag = prop.tag.split('}')
            propTag = propTag[len(propTag) - 1]

            if propTag == 'key':
                keyName = prop.attrib['value']
                break

        self.keyName = keyName
        self.name = xmlElem.attrib['name']
        self.nodeType = NODE_TYPE_CONTAINER
        self.path = path
        self.children = []


    def getRecursiveCppChildHeader(self):
        header = ''

        for child in self.children:
            header += child.getRecursiveCppChildHeader()

        header += 'class ' + yangName2ClassName(self.name) + ' : BasicNode {\n'
        header += '   public:\n'
        header += '    ' + yangName2ClassName(self.name) + ' : BasicNode("' + self.path + '") {}\n'
        header += '\n'
        header += '   private:\n'
        for child in self.children:
            header += child.getCppInstantiate('    ')
        header += '};\n\n'

        return header

    def getCppInstantiate(self, preIdent = ''):
        return preIdent + 'std::map<Leaf<' + self.key.getType() + '>, ' + yangName2ClassName(self.name) + '>' + ' ' + yangName2VarName(self.name) + ';\n'

    def getPath(self):
        return self.path

    def getName(self):
        return self.name

    def addChildNode(self, child):
        # If it's the key of the list, save it as the key, not as a normal child
        if child.getName() == self.keyName:
            self.key = child
            return

        self.children.append(child)

    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'List ' + self.name + ' [ ' + self.key.getType() + ' ' + self.key.getName() + ' ]'
        print prePrintLine + '|   Path: ' + self.path
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

####################################################################################################

DataNodeTypes = {
    NODE_TYPE_MODULE : Module,
    NODE_TYPE_LEAF : Leaf,
    NODE_TYPE_CONTAINER : Container,
    NODE_TYPE_LIST : List,
}

####################################################################################################

def createNode(xmlElem, path):
    tag = xmlElem.tag.split('}')
    tag = tag[len(tag) - 1]

    if not (tag in DataNodeTypes):
        return None

    currentPath = path + xmlElem.attrib['name'] + '/'
    node = DataNodeTypes[tag](xmlElem, currentPath)

    return node

####################################################################################################

def IterateOverNode(parentNode, xmlElem, path = '/'):
    for child in xmlElem:
        node = createNode(child, path)
        if node == None:
            continue

        parentNode.addChildNode(node)
        IterateOverNode(node, child, node.getPath())

####################################################################################################


rootNode = createNode(root, '')
IterateOverNode(rootNode, root)

#rootNode.showRecursive()


print rootNode.getRecursiveCppHeader()
