# -*- coding: utf-8 -*-
"""
@author: ashwinkumars
"""

import time
import logging

from ABADocumentCreater import create_document_for_simulation
from ABAUtils import sanitize_docs
from ABAUtils import get_assigned_dev_and_delta
from ABAUtils import algo1
from ABAUtils import get_similarity_vector

logger = logging.getLogger(__name__)

def run_sim_ABA(devDocDict, queryDocDict) :
    count = 0;
    truePrediction = 0;
    devMap = {}
    assignedDev = ""
    allDocuments = [] 
    
    for dev, documents in devDocDict.items() :
        allDocuments.extend(documents)
        devMap[dev] = len(documents)     
        
    tfidfRepresentation, idf = algo1(allDocuments) 
    totalDelta = 0;    
    
    for dev, queryDoc in queryDocDict.items() :
        localCount = 0
        localPrediction = 0
        for query in queryDoc :                
            localCount = localCount + 1                
            similarityVector = get_similarity_vector(tfidfRepresentation, idf, query)  
            assignedDev, delta = get_assigned_dev_and_delta(similarityVector, devMap, dev)
            totalDelta = totalDelta + delta
                
            count = count + 1
            if assignedDev == dev :
                truePrediction = truePrediction + 1
                localPrediction = localPrediction + 1
            #else :               
                #logger.info(assigned_dev + " != " + dev)
                    
        logger.info(dev + ":" + str(localPrediction) + "/" + str(localCount))
        logger.debug("total current : " + str(truePrediction * 100 / count))
            
    
    #logger.info("ave delta : " + str(totalDelta / count))
    logger.info("Prediction result : " + str(truePrediction * 100 / count))

def execute_sim(dataABA) :
    start = time.time()
    logger.info('Simulation started for file : ' + dataABA.docPath + '.')
 
    devDocDict, queryDocDict = create_document_for_simulation(dataABA)
 
    devDocDictCleaned = {}
    queryDocDictCleaned = {}
    
    #remove empty dev with no docs
    for dev, allDocuments in devDocDict.items() :                
        allDocuments = sanitize_docs(allDocuments)        
        if len(allDocuments) > 0 :
            devDocDictCleaned[dev] = allDocuments   
            
    for dev, allDocuments in queryDocDict.items() :                
        allDocuments = sanitize_docs(allDocuments)        
        if len(allDocuments) > 0 :
            queryDocDictCleaned[dev] = allDocuments    
    
    run_sim_ABA(devDocDictCleaned, queryDocDictCleaned)    
    
    end = time.time()
    logger.info("Total time : " + str(end - start) + '\n')
    logger.info('Simulation complete for ' + dataABA.docPath + '.')
