# -*- coding: utf-8 -*-
"""
@author: ashwinkumars
"""

import xml.etree.ElementTree as ElemTree
import logging

from ABADocumentCreater import ABAInputs

SIMULATE = 'simulate'
TRAIN = 'train'
QUERY = 'query'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_node_attribute_value(node, attribute) :
    value = ''
    if node != None :
        value = node.get(attribute)
        
    return value

def get_node_value(parentNode, nodeName) :
    value = ''
    if parentNode != None :
        childNode = parentNode.find(nodeName)
        
        if childNode != None :
            value = childNode.text
        
    return value

def get_node_atribute_value(parentNode, nodeName, attribute) :
    value = ''
    if parentNode != None :
        childNode = parentNode.find(nodeName)
        
        if childNode != None :
            value = childNode.get(attribute)
        
    return value

# =============================================================================
# <data>
#     <item type='simulate' value='true'>
#         <docPath sheetName='sheetName1'>docfile1</docPath>		
#         <devColName>Assignee</devColName>
#         <descColName>Summary</descColName>
#         <trainDataFraction>0.8</trainDataFraction>
#     </item>
#     <item type='simulate' value='false'>
#         <docPath sheetName='sheetName2'>docfile2</docPath>
#         <devColName>Assignee</devColName>
#         <descColName>Summary,Product,Component</descColName>
#         <trainDataFraction>0.8</trainDataFraction>
#     </item>    
# 	<item type='train' value='true'>
#         <docPath sheetName='sheetName3'>docfile3</docPath>
#         <devColName>Assignee</devColName>
#         <descColName>Summary</descColName>
#         <trainOutputFile>trainingdb_output_file</trainOutputFile>
#     </item>    
#     <item type='query' value='false'>
#         <docPath sheetName='sheetName4'>docfile4</docPath>
# 		<devColName>Assignee</devColName>
# 		<descColName>col1, col2, ....</descColName>
# 		<bugIdColName>Bug ID</bugIdColName>
#         <trainInputFile>trainingdb_input_file</trainInputFile>
#     </item>	
#     .
#     .
# </data>
# =============================================================================
def load_input_data(inputFile, dataType) :
    dataABAList = []    
    tree = ElemTree.parse(inputFile)  
    root = tree.getroot()    
   
    for item in root :
        inputType = ''
        docPath = ''
        sheetName = ''
        devColName = ''
        descColName = ''
        trainFilePath = ''
        docIdColName = ''
        trainDataFraction = 100.0    
        
        inputType = get_node_attribute_value(item, 'type')
        if inputType != dataType or get_node_attribute_value(item, 'value') != 'true' :
            continue
        
        docPath = get_node_value(item, 'docPath')
        sheetName = get_node_atribute_value(item, 'docPath', 'sheetName')
        if sheetName == '' :
            sheetName = 0
        
        devColName = get_node_value(item, 'devColName')
        descColName = list(get_node_value(item, 'descColName').split(','))       
        
        if inputType == TRAIN :
            trainFilePath = get_node_value(item, 'trainOutputFile')
        elif inputType == QUERY :
            trainFilePath = get_node_value(item, 'trainInputFile') 
            docIdColName = get_node_value(item, 'bugIdColName')
      
        if inputType == SIMULATE :
            trainDataFraction = float(get_node_value(item, 'trainDataFraction'))        
            
        dataABA = ABAInputs(inputType, docPath, sheetName, 
                            devColName, descColName, trainFilePath, 
                            docIdColName, trainDataFraction)
        dataABAList.append(dataABA)
    
    return dataABAList

def load_dev_map(devListNode):
    devMap = {}
    
    for devNode in devListNode :
        name = devNode.get('name')
        count = int(devNode.get('count'))
        devMap[name] = count

    return devMap

def load_idf(idfNode):
    idf = {}
    
    for termNode in idfNode :
        name = termNode.get('name')
        value = float(termNode.text)
        idf[name] = value 
    
    return idf

def load_tfidf(tfidfNode):
    tfidfRepresentation = []
    
    for docNode in tfidfNode :
        doc = list(docNode.text.split(','))         
        docNum = [float(x) for x in doc]
        tfidfRepresentation.append(docNum)    
    
    return tfidfRepresentation

# =============================================================================
# <data>
# 	<item>
# 		<devlist>
#         <dev count='n1', name='dev1'></dev>
#         <dev count='n2', name='dev2'></dev>
#         .
#         .
#      </devlist>
# 		<idf>
# 			<term name='word1'>value1</term>
# 			<term name='word2'>value2</term>
#         .
#         .
# 		</idf>
# 		<tfidf>
# 			<doc>value_word1, value_word2, ....</doc>
# 			<doc>value_word1, value_word2, ....</doc>
# 		</tfidf>
# 	</item>
#   .
#   .
# </data>
# 
# =============================================================================
def load_training_data(trainInputFile) :
    devMap = load_dev_map
    idf = load_idf
    tfidfRepresentation = load_tfidf
    
    tree = ElemTree.parse(trainInputFile)  
    root = tree.getroot()   
    item = root.find('item')
    
    devMap = load_dev_map(item.find('devlist'))
    idf = load_idf(item.find('idf'))
    tfidfRepresentation = load_tfidf(item.find('tfidf'))
    
    return devMap, idf, tfidfRepresentation
