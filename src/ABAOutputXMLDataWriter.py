# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 18:51:40 2018

@author: ashwinkumars
"""

import xml.etree.ElementTree as ElemTree
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# <data>
# 	<item>
# 		<devlist>
#         <dev name='dev1', count='n'></dev>
#         <dev name='dev1', count='n'></dev>
#      </devlist>
# 		<idf>
# 			<term name='word1'>value1</term>
# 			<term name='word2'>value2</term>
# 		</idf>
# 		<tfidf>
# 			<doc>value_word1, value_word2, ....</doc>
# 			<doc>value_word1, value_word2, ....</doc>
# 		</tfidf>
# 	</item>
# </data>
# 
# =============================================================================
def write_train_data(devMap, tfidfRepresentation, idf, trainFilePath) :      
    dataNode = ElemTree.Element('data')
    itemNode = ElemTree.SubElement(dataNode, 'item') 
    devlistNode = ElemTree.SubElement(itemNode, 'devlist') 
    idfNode = ElemTree.SubElement(itemNode, 'idf') 
    tfidfNode = ElemTree.SubElement(itemNode, 'tfidf')    
    
    #add dev names to tree  
    for dev, count in devMap.items() :
        devNode = ElemTree.SubElement(devlistNode, 'dev')
        devNode.set('name', dev)        
        devNode.set('count', str(count))         
    
    #add idf values to tree
    for term, val in idf.items() :
        termNode = ElemTree.SubElement(idfNode, 'term')
        termNode.set('name', term)
        termNode.text = str(val)
        
    #add tfidf values to tree
    for li in tfidfRepresentation :        
        docNode = ElemTree.SubElement(tfidfNode, 'doc')
        docStr = ",".join([str(x) for x in li])
        docNode.text = docStr
    
    
    xmlstr  = ElemTree.tostring(dataNode, encoding='unicode')    
    file = open(trainFilePath, "w")  
    file.write(xmlstr) 
    file.close()
    