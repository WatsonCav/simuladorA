# -*- encoding: utf-8 -*-
from xml.etree import ElementTree
from xml.dom import minidom
from PySide import QtCore, QtGui
from graphics import Node, Edge

class DiagramToXML(ElementTree.Element):
    '''
        Esta classe possui as funções que armazenam as informações
        necessárias à reconstrução do diagrama grafico em um
        arquivo XML
    '''
    def __init__(self, scene):
        '''
            Função que inicializa o objeto criado pela classe DiagramToXML
        '''
        super(DiagramToXML, self).__init__('items')
        
        self.scene = scene
        lista = self.scene.items()
        lista.reverse()
        for item in self.scene.items():
            if isinstance(item, Node):
                node = ElementTree.Element('node', attrib={'type' : str(item.myItemType) })
                id = ElementTree.Element('id')
                id.text = str(item.id)
                node.append(id)
                
                x = ElementTree.Element('x')
                x.text = str(item.scenePos().x())
                node.append(x)
                
                y = ElementTree.Element('y')
                y.text = str(item.scenePos().y())
                node.append(y)
                
                width = ElementTree.Element('width')
                width.text = str(item.rect().width())
                node.append(width)
                
                height = ElementTree.Element('height')
                height.text = str(item.rect().height())
                node.append(height)
                
                self.append(node)
        for item in lista:
            
            if isinstance(item, Edge):
                edge = ElementTree.Element('edge')
                w1 = ElementTree.Element('w1')
                w1.text = str(item.w1.id)
                
                
                w2 = ElementTree.Element('w2')
                w2.text = str(item.w2.id)
                edge.append(w1)
                edge.append(w2)
                self.append(edge)
                print str(item.w1.id),str(item.w2.id)
    
    def writeXML(self, path):
        '''
            Função que cria o arquivo XML na localização indicada pelo
            argumento path
        '''
        xmlString = ElementTree.tostring(self)
        domElement = (minidom.parseString(xmlString))
        f = open(path, 'w')
        f.write(domElement.toprettyxml())
        f.close()

class XMLToDiagram():
    '''
        Classe que realiza a convesão do arquivo XML com as informações do diagrama
        em um diagrama gráfico interativo
    '''
    def __init__(self, scene, filePath):
        self.scene = scene
        self.filePath = filePath
        
        xmlTree = ElementTree.parse(self.filePath)
        xmlElement = xmlTree.getroot()
        print xmlElement
        self.scene.clear()
        for child in xmlElement:
            
            if child.tag == 'node':
                
                if child.attrib['type'] == '0':
                    item = Node(int(child.attrib['type']), self.scene.mySubstationMenu)
                    self.scene.addItem(item)
                    item.setPos(float(child.find('x').text), float(child.find('y').text))
                    item.id = int(child.find('id').text)
                    
                    
                elif child.attrib['type'] == '1':
                    item = Node(int(child.attrib['type']), self.scene.myRecloserMenu)
                    item.id = int(child.find('id').text)
                    item.setPos(float(child.find('x').text), float(child.find('y').text))                    
                    self.scene.addItem(item)
                    
                elif child.attrib['type'] == '2':
                    item = Node(int(child.attrib['type']), self.scene.myBusMenu)
                    item.setPos(float(child.find('x').text), float(child.find('y').text))
                    item.id = int(child.find('id').text)
                    item.setRect(0, 0, float(child.find('width').text), float(child.find('height').text))
                    self.scene.addItem(item)
                    
                elif child.attrib['type'] == '3':
                    item = Node(int(child.attrib['type']), None)
                    item.setPos(float(child.find('x').text), float(child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)
                    
            elif child.tag == 'edge':
    
                for item in self.scene.items():
                    if isinstance(item, Node) and item.id == int(child.find('w1').text):
                        w1 = item
                        print item.id
                    elif isinstance(item, Node) and item.id == int(child.find('w2').text):
                        w2 = item
                        print item.id
                print w1.id,w2.id
                edge = Edge(w1, w2,self.scene.myLineMenu)
                self.scene.addItem(edge)
                self.scene.addItem(edge.ghostRetItem)
                #edge.updateRet()
