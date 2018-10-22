# -*- coding: utf-8 -*-
"""
@author: ashwinkumars
"""

import time
import logging
from ABADocumentCreater import create_document_for_train
from ABAUtils import sanitize_docs
from ABAUtils import algo1
from ABAOutputXMLDataWriter import write_train_data

logger = logging.getLogger(__name__)

def run_train_ABA(devDocDict) :    
    devMap = {}    
    allDocuments = [] 
    
    for dev, documents in devDocDict.items() :
        allDocuments.extend(documents)
        devMap[dev] = len(documents)     

    tfidfRepresentation, idf = algo1(allDocuments)
    return devMap, tfidfRepresentation, idf   

def execute_train(dataABA) :
    devDocDictCleaned = {}
    
    start = time.time()
    logger.info('Training started for file : ' + dataABA.docPath + '.')
 
    devDocDict = create_document_for_train(dataABA) 
   
    #remove empty dev with no docs
    for dev, allDocuments in devDocDict.items() :                
        allDocuments = sanitize_docs(allDocuments)        
        if len(allDocuments) > 0 :
            devDocDictCleaned[dev] = allDocuments    
   
    devMap, tfidfRepresentation, idf = run_train_ABA(devDocDictCleaned)    
    
    end = time.time()
    logger.info("Total time :" + str(end - start) + '\n')
    logger.info('Training complete for ' + dataABA.docPath + '.')
    
    return devMap, tfidfRepresentation, idf
    
def execute_train_and_dump_data(dataABA) :   
    devMap, tfidfRepresentation, idf = execute_train(dataABA)
    write_train_data(devMap, tfidfRepresentation, idf, dataABA.trainFilePath)
    
    