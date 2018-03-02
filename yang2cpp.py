#!/usr/bin/python
import xml.etree.ElementTree as ET
import argparse
import subprocess
import sys

# Node types strings
NODE_TYPE_MODULE    = 'module'
NODE_TYPE_LEAF      = 'leaf'
NODE_TYPE_CONTAINER = 'container'
NODE_TYPE_AUGMENT   = 'augment'
NODE_TYPE_LIST      = 'list'
NODE_TYPE_LEAFLIST  = 'leaf-list'
NODE_TYPE_USES      = 'uses'

# Conversion from YANG types to C++ types
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
## Convert a YANG node name in a C++ Class name
# @param  yangName  YANG node name
def yangName2ClassName(yangName):
    return yangName.title().replace('-', '').replace('_', '')

####################################################################################################
## Convert a YANG node name in a C++ variable/attribute name
# @param  yangName  YANG node name
def yangName2VarName(yangName):
    return yangName.lower().replace('-', '_') + '_'

####################################################################################################
## Generic node representation
class Node(object):

    ################################################################################################
    ## Constructor
    # @param  self     The current object
    # @param  xmlElem  XML Element representing the node to be created
    # @param  path     The path of the node
    def __init__(self, xmlElem, path):
        if 'name' in xmlElem.attrib:
           self.name = xmlElem.attrib['name']
        self.path = path
        self.children = []
        self.valueType = ''
        self.key = ''
        self.description = ''

    ################################################################################################
    ## Retrieve the node name
    # @param  self  The current object
    # return  Node name
    def getName(self):
        return self.name

    ################################################################################################
    ## Retrieve the node path
    # @param  self  The current object
    # return  Node path
    def getPath(self):
        return self.path

    ################################################################################################
    ## Set description to node
    # @param  self  The current object
    # @param  desc  Description to be set
    def setDescription(self, desc):
        self.description = desc

    ################################################################################################
    ## Add a child to the current node
    # @param  self   The current object
    # @param  child  Child to be added
    def addChildNode(self, child):
        self.children.append(child)

    ################################################################################################
    ## Retrieve a string containing the line of the leaf C++ instantiation
    # @param  self  The current object
    # return  String containing the line of the leaf instantiation
    def getCppInstantiate(self):
        if self.valueType:
            return '    CppYangModel::Leaf<' + YangTypeConversion[self.valueType] + '>' + ' '\
                   + yangName2VarName(self.name) + ';\n'

        if self.key:
            return '    std::map<CppYangModel::Leaf<' + YangTypeConversion[self.key.getType()]\
                   + '>, ' + yangName2ClassName(self.name) + '>' + ' '\
                   + yangName2VarName(self.name) + ';\n'

        if self.name:
            return '    ' + yangName2ClassName(self.name) + ' ' + yangName2VarName(self.name)\
                   + ';\n'

        return ''

    ################################################################################################
    ## Retrieve a string containing the line of the container C++ object initialization
    # @param  self  The current object
    # return  Empty string, since the initialization is not needed
    def getCppInitializer(self):
        return ""

####################################################################################################
## Leaf representation
class Leaf(Node):

    ################################################################################################
    ## Constructor
    # @param  self     The current object
    # @param  xmlElem  XML Element representing the leaf to be created
    # @param  path     The path of the leaf
    def __init__(self, xmlElem, path):
        super(Leaf, self).__init__(xmlElem, path)

        # Get type of leaf
        valueType = ''
        for prop in xmlElem:
            propTag = prop.tag.split('}')
            propTag = propTag[len(propTag) - 1]

            if propTag == 'type':
                valueType = prop.attrib['name']
                break

        self.valueType = valueType

    ################################################################################################
    ## Retrieve a string containing the recursive C++ header
    # @param  self  The current object
    # return  An empty string
    def getRecursiveCppHeader(self):
        return ''

    ################################################################################################
    ## Retrieve a string containing the recursive C++ implementation
    # @param  self  The current object
    # return  An empty string
    def getRecursiveCppImplementation(self):
        return ''

    ################################################################################################
    ## Retrieve a string containing the line of the leaf C++ object initialization
    # @param  self  The current object
    # return  String containing the line of the leaf C++ object initialization
    def getCppInitializer(self):
        return yangName2VarName(self.name) + '("' + self.path + '")'

    ################################################################################################
    ## Retrieve the leaf value
    # @param  self  The current object
    # return  The leaf value
    def getType(self):
        return self.valueType

    ################################################################################################
    ## Retrieve a string containing a representation of the leaf. Used for debug purposes
    # @param  self          The current object
    # @param  prePrintLine  String the must be printed before each line (indentation)
    # return  String containing the leaf representations
    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Leaf ' + self.name
        print prePrintLine + '|   Type: ' + self.valueType
        print prePrintLine + '|   Path: ' + self.path
        print prePrintLine + '\''

####################################################################################################
## Container representation
class Container(Node):

    ################################################################################################
    ## Constructor
    # @param  self     The current object
    # @param  xmlElem  XML Element representing the leaf to be created
    # @param  path     The path of the leaf
    def __init__(self, xmlElem, path):
        super(Container, self).__init__(xmlElem, path)

    ################################################################################################
    ## Retrieve a string containing the recursive C++ header, including the headers of its children
    # @param  self  The current object
    # return  String containing the recursive C++ header
    def getRecursiveCppHeader(self):
        header = ''
        instantiationList = ''

        for child in self.children:
            header += child.getRecursiveCppHeader()
            instantiationList += child.getCppInstantiate()

        header += '/******************************************************************************'\
               + '********************/\n'
        header += '/**\n'
        header += ' * \\brief ' + self.description + '\n'
        header += ' */\n'
        header += 'class ' + yangName2ClassName(self.name) + ' : public CppYangModel::BasicNode {\n'
        header += '   public:\n'
        header += '    /**\n'
        header += '     * \\brief Constructor\n'
        header += '     */\n'
        header += '    ' + yangName2ClassName(self.name) + '();\n'
        header += '\n'

        if instantiationList != '':
            header += '   private:\n'
            header +=      instantiationList

        header += '};\n\n'

        return header

    ################################################################################################
    ## Retrieve a string containing the recursive C++ implementation, including its children
    # @param  self  The current object
    # return  String containing the recursive C++ implementation
    def getRecursiveCppImplementation(self):
        impl = ''
        initializerList = ''

        for child in self.children:
            impl += child.getRecursiveCppImplementation()
            initializer = child.getCppInitializer()
            if initializer != '':
                initializerList += ',\n    ' + child.getCppInitializer()

        impl += '/******************************************************************************'\
               + '********************/\n\n'
        impl += yangName2ClassName(self.name) + '::' + yangName2ClassName(self.name) + '()\n'
        impl += '    : CppYangModel::BasicNode("' + self.path + '")'

        ## If initializer list is not empty, print it
        if initializerList != '':
            impl +=  initializerList + '\n'

        impl += '{\n'
        impl += '}\n'
        impl += '\n'

        return impl


    ################################################################################################
    ## Retrieve a string containing a representation of the container. Used for debug purposes
    # @param  self          The current object
    # @param  prePrintLine  String the must be printed before each line (indentation)
    # return  String containing the container representations
    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Container ' + self.name
        print prePrintLine + '|   Path: ' + self.path
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

####################################################################################################
## List representation
class List(Container):

    ################################################################################################
    ## Constructor
    # @param  self     The current object
    # @param  xmlElem  XML Element representing the leaf to be created
    # @param  path     The path of the leaf
    def __init__(self, xmlElem, path):
        super(List, self).__init__(xmlElem, path)
        # Get key
        keyName = ''
        for prop in xmlElem:
            propTag = prop.tag.split('}')
            propTag = propTag[len(propTag) - 1]

            if propTag == 'key':
                keyName = prop.attrib['value']
                break

        self.keyName = keyName

    ################################################################################################
    ## Add a child to the current node instead of the child is the key
    # @param  self   The current object
    # @param  child  Child to be added
    def addChildNode(self, child):
        # If it's the key of the list, save it as the key, not as a normal child
        if child.getName() == self.keyName:
            self.key = child
            return

        self.children.append(child)

    ################################################################################################
    ## Retrieve a string containing a representation of the list. Used for debug purposes
    # @param  self          The current object
    # @param  prePrintLine  String the must be printed before each line (indentation)
    # return  String containing the list representations
    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'List ' + self.name + ' [ ' + self.key.getType() + ' '\
              + self.key.getName() + ' ]'
        print prePrintLine + '|   Path: ' + self.path
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

####################################################################################################
## Augment representation
class Augment(Container):

    ################################################################################################
    ## Constructor
    # @param  self     The current object
    # @param  xmlElem  XML Element representing the leaf to be created
    # @param  path     The path of the leaf
    def __init__(self, xmlElem, path):
        super(Augment, self).__init__(xmlElem, xmlElem.attrib['target-node'] + '/')
        self.name = xmlElem.attrib['target-node'][1:].title().replace(":", "_").replace("-", "_")\
                    .replace("/", "__")

    ################################################################################################
    ## Retrieve a string containing a representation of the augment. Used for debug purposes
    # @param  self          The current object
    # @param  prePrintLine  String the must be printed before each line (indentation)
    # return  String containing the augment representations
    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Augment ' + self.path
        print prePrintLine + '|   Path: ' + self.path
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

####################################################################################################
## Module representation
class Module(Node):

    ################################################################################################
    ## Constructor
    # @param  self     The current object
    # @param  xmlElem  XML Element representing the leaf to be created
    # @param  path     The path of the leaf
    def __init__(self, xmlElem, path='/'):
        super(Module, self).__init__(xmlElem, path)
        self.nodeType = NODE_TYPE_MODULE

    ################################################################################################
    ## Retrieve a string containing the recursive C++ header, including the headers of its children
    # @param  self  The current object
    # return  String containing the recursive C++ header
    def getRecursiveCppHeader(self):
        header = ''
        instantiationList = ''

        for child in self.children:
            header += child.getRecursiveCppHeader()
            instantiationList += child.getCppInstantiate()

        header += '/******************************************************************************'\
               + '********************/\n'
        header += '/**\n'
        header += ' * \\brief ' + self.description + '\n'
        header += ' */\n'
        header += 'class ' + yangName2ClassName(self.name) + ' {\n'
        header += '   public:\n'
        header += '    /**\n'
        header += '     * \\brief Constructor\n'
        header += '     */\n'
        header += '    ' + yangName2ClassName(self.name) + '();\n'
        header += '\n'

        # If instantiation list is not empty, print it
        if instantiationList != '':
            header += '   private:\n'
            header += instantiationList

        header += '};'

        return header

    ################################################################################################
    ## Retrieve a string containing the recursive C++ implementation, including its children
    # @param  self  The current object
    # return  String containing the recursive C++ implementation
    def getRecursiveCppImplementation(self):
        impl = ''
        initializerList = ''

        for child in self.children:
            impl += child.getRecursiveCppImplementation()

            initializer = child.getCppInitializer()
            if initializerList != '' and initializer != '':
                initializerList += ',\n        '

            initializerList += initializer

        impl += '/******************************************************************************'\
               + '********************/\n\n'
        impl += yangName2ClassName(self.name) + '::' + yangName2ClassName(self.name) + '()\n'

        # If initializer list is not empty, print it
        if initializerList != '':
            impl += '    : ' + initializerList + '\n'

        impl += '{\n'
        impl += '}\n'

        return impl

    ################################################################################################
    ## Retrieve a string containing a representation of the module. Used for debug purposes
    # @param  self          The current object
    # @param  prePrintLine  String the must be printed before each line (indentation)
    # return  String containing the module representations
    def showRecursive(self, prePrintLine = ''):
        print prePrintLine + 'Module ' + self.name
        for child in self.children:
            child.showRecursive(prePrintLine + '|   ')
        print prePrintLine + '\''

####################################################################################################

# Dictionary that maps YANG node type to the related handler class
DataNodeTypes = {
    NODE_TYPE_MODULE : Module,
    NODE_TYPE_LEAF : Leaf,
    NODE_TYPE_CONTAINER : Container,
    NODE_TYPE_LIST : List,
    NODE_TYPE_AUGMENT : Augment,
}

####################################################################################################
## Handle a description
# @param  xmlElem  XML node of description
# @param  parent   Parent node
# return  The parent with changes
def handleDescription(xmlElem, parent):
    parent.setDescription(xmlElem[0].text);
    return parent

####################################################################################################

# Dictionary that maps properties to handler
PropertiesToHandler = {
    'description' : handleDescription,
}

####################################################################################################
## Create a node
# @param  xmlElem  XML element
# @param  path     Base path
# return  The created node
def createNode(xmlElem, path):
    tag = xmlElem.tag.split('}')
    tag = tag[len(tag) - 1]

    if not (tag in DataNodeTypes):
        return None

    currentPath = ''
    if 'name' in xmlElem.attrib:
        currentPath = path + xmlElem.attrib['name'] + '/'
    node = DataNodeTypes[tag](xmlElem, currentPath)

    return node

####################################################################################################
## Iterate over XML element recursively creating nodes
# @param  parentNode  Parent node
# @param  xmlElem     XML element
# @param  path        Base path
def iterateOverNode(parentNode, xmlElem, path = '/'):
    for child in xmlElem:

        node = createNode(child, path)
        if node != None:
            parentNode.addChildNode(node)
        else:
            tag = child.tag.split('}')
            tag = tag[len(tag) - 1]

            if tag in PropertiesToHandler:
                parentNode = PropertiesToHandler[tag](child, parentNode)

            continue

        iterateOverNode(node, child, node.getPath())

####################################################################################################

# Arguments parsing
parser = argparse.ArgumentParser(description='Convert a given YANG model in a C++ classes model.')
parser.add_argument('-o', '--output', type=str, metavar='PREFIX',
                    help='Output prefix. Two files (a .h and a .cc) will be created based on this '
                          'prefix. The default is the YANG module name.')
parser.add_argument('-d', '--output-directory', type=str, metavar='DIR',
                    help='Path to directory where the output files will be placed in. The default '
                         'is the current directory.', default='./')
parser.add_argument('-p', '--path', type=str, metavar='PATH1:PATH2', action='append',
                    help='path is a colon (:) separated list of directories to search for imported '
                         'modules. This option may be given multiple times.')
parser.add_argument('input', type=str, help='YANG file to be converted.')
args = parser.parse_args()

# Mount pybot command
cmd = ["pyang", args.input, "-f", "yin", "-o", args.input + ".xml"]
if args.path:
    for path in args.path:
        cmd.append("-p")
        cmd.append(path)
if subprocess.call(cmd) != 0:
    sys.exit("Error parsing input file: " + args.input)


# Open generated XML
tree = ET.parse(args.input + ".xml")
root = tree.getroot()

# Parse it
rootNode = createNode(root, '')
iterateOverNode(rootNode, root)


header = '/**************************************************************************************'\
       + '************/\n'
header += '/**\n'
header += ' * \\file\n'
header += ' * \\brief ' + rootNode.getName() + ' YANG module representation.\n'
header += ' *\n'
header += ' * WARNING WARNING --> This is an auto generated file <-- WARNING WARNING\n'
header += ' *\n'
header += ' */\n'
header += '/**************************************************************************************'\
       + '************/\n\n'

# Generate header file
headerContent = header
headerContent += '#ifndef __AUTOGEN_' + rootNode.getName().upper() + '_H__\n'
headerContent += '#define __AUTOGEN_' + rootNode.getName().upper() + '_H__\n'
headerContent += '\n'
headerContent += '#include "yang2cpp.h"\n'
headerContent += '\n'
headerContent += rootNode.getRecursiveCppHeader()
headerContent += '\n'
headerContent += '#endif /* __AUTOGEN_' + rootNode.getName().upper() + '_H__ */\n'
outputFile = rootNode.getName()
if args.output:
    outputFile = args.output
outputFile += '.h'
f = open(args.output_directory + '/' + outputFile, 'w')
f.write(headerContent)
f.close


# Generate implementation
implementationContent = header
implementationContent += '#include "' + outputFile + '"\n'
implementationContent += '\n'
implementationContent += rootNode.getRecursiveCppImplementation()
outputFile = rootNode.getName()
if args.output:
    outputFile = args.output
outputFile += '.cc'
f = open(args.output_directory + '/' + outputFile, 'w')
f.write(implementationContent)
f.close

# Generate basic header
basicHeader  = '/*********************************************************************************'\
               '*****************/\n'
basicHeader += '/**\n'
basicHeader += ' * \\file\n'
basicHeader += ' * \\brief Basics classes used in YANG generator\n'
basicHeader += ' *\n'
basicHeader += ' * WARNING WARNING --> This is an auto generated file <-- WARNING WARNING\n'
basicHeader += ' *\n'
basicHeader += ' */\n'
basicHeader += '/*********************************************************************************'\
               '*****************/\n'
basicHeader += '\n'
basicHeader += '#ifndef __YANG2CPP_H__\n'
basicHeader += '#define __YANG2CPP_H__\n'
basicHeader += '\n'
basicHeader += '#include <string>\n'
basicHeader += '#include <map>\n'
basicHeader += '#include <stdint.h>\n'
basicHeader += '\n'
basicHeader += '/*********************************************************************************'\
               '*****************/\n'
basicHeader += '\n'
basicHeader += 'namespace CppYangModel {\n'
basicHeader += '\n'
basicHeader += '/**\n'
basicHeader += ' * \\brief Basic generic node\n'
basicHeader += ' */\n'
basicHeader += 'class BasicNode {\n'
basicHeader += '   public:\n'
basicHeader += '    /**\n'
basicHeader += '     * \\brief Constructor\n'
basicHeader += '     * \param path  Path of the node\n'
basicHeader += '     */\n'
basicHeader += '    BasicNode(std::string path) : path_(path) {}\n'
basicHeader += '\n'
basicHeader += '   private:\n'
basicHeader += '    std::string path_;\n'
basicHeader += '};\n'
basicHeader += '\n'
basicHeader += '/*********************************************************************************'\
               '*****************/\n'
basicHeader += '/**\n'
basicHeader += ' * \\brief Leaf of the tree\n'
basicHeader += ' */\n'
basicHeader += 'template <class T>\n'
basicHeader += 'class Leaf : public BasicNode {\n'
basicHeader += '   public:\n'
basicHeader += '    /**\n'
basicHeader += '     * \\brief Constructor\n'
basicHeader += '     * \param path  Path of the leaf\n'
basicHeader += '     */\n'
basicHeader += '    Leaf(std::string path) : BasicNode(path) {}\n'
basicHeader += '\n'
basicHeader += '    /**\n'
basicHeader += '     * \\brief Set path of the leaf\n'
basicHeader += '     * \param path  Path to be set\n'
basicHeader += '     */\n'
basicHeader += '    void setValue(const T& value) {\n'
basicHeader += '        value_ = value;\n'
basicHeader += '    }\n'
basicHeader += '\n'
basicHeader += '    /**\n'
basicHeader += '     * \\brief Get path of the leaf\n'
basicHeader += '     * \\return Path of the list\n'
basicHeader += '     */\n'
basicHeader += '    T getValue() {\n'
basicHeader += '        return value_;\n'
basicHeader += '    }\n'
basicHeader += '\n'
basicHeader += '   private:\n'
basicHeader += '    T value_;\n'
basicHeader += '};\n'
basicHeader += '\n'
basicHeader += '} /* namespace CppYangModel */\n'
basicHeader += '\n'
basicHeader += '#endif /* __YANG2CPP_H__ */\n'
f = open(args.output_directory + '/yang2cpp.h', 'w')
f.write(basicHeader)
f.close
