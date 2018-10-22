# -*- coding: utf-8 -*-
"""
@author: ashwinkumars
"""

import pandas as pd
import collections
import logging

logger = logging.getLogger(__name__)

COMBINED_DOC_COL = 'combinedDocCol'

ABAInputs = collections.namedtuple("ABAInputs", 
                                   "inputType docPath sheetName devColName descColName \
                                   trainFilePath docIdColName trainDataFraction")

def get_dev_list(data, devColName) :
    assigneeList = sorted([item for item in data[devColName].unique() if item == item]) 
    
    return assigneeList

def create_data(docPath, sheetName) :
    data = pd.read_excel(docPath, sheetName)    
    data.fillna('')   
    
    return data

def create_data_and_combine_column(dataABA) :
    data = create_data(dataABA.docPath, dataABA.sheetName)
    data[COMBINED_DOC_COL] = ''
    for item in dataABA.descColName :        
        data[COMBINED_DOC_COL] = data[COMBINED_DOC_COL] + ' ' + data[item]

    return data    

def create_document_for_simulation(dataABA) :
    devDocDict = {}
    queryDocDict = {}   
    removedList = []
    trainDataCount = 0
    testDataCount = 0

    data = create_data_and_combine_column(dataABA)        
    assigneeList = get_dev_list(data, dataABA.devColName)   
        
    traindata = data.sample(frac = dataABA.trainDataFraction, random_state = 200)
    testdata = data.drop(traindata.index)  
    
    for dev in assigneeList :       
        dataDev = traindata.loc[traindata[dataABA.devColName] == dev].copy()       
     
        if(dataDev[COMBINED_DOC_COL].count() > 0 ) :     
            trainDataCount = trainDataCount + dataDev[COMBINED_DOC_COL].count() 
            devDocDict[dev] = list(dataDev[COMBINED_DOC_COL])
        else :
            removedList.append(dev)
          
    for dev in assigneeList :
        dataDev = testdata.loc[testdata[dataABA.devColName] == dev].copy()       
     
        if(dataDev[COMBINED_DOC_COL].count() > 0 and dev not in removedList) :
            testDataCount = testDataCount + dataDev[COMBINED_DOC_COL].count()                
            queryDocDict[dev] = list(dataDev[COMBINED_DOC_COL])   
    
    logger.info("Ratio of traindata : testdata = " + str(trainDataCount) + " : " + str(testDataCount))
    
    return devDocDict, queryDocDict

def create_document_for_train(dataABA) :
    devDocDict = {}   
    
    data = create_data_and_combine_column(dataABA)
    
    assigneeList = get_dev_list(data, dataABA.devColName)    
    logger.info("traindata set = " + str(len(data)))    
    
    for dev in assigneeList :       
        dataDev = data.loc[data[dataABA.devColName] == dev].copy()       
     
        if(dataDev[COMBINED_DOC_COL].count() > 0 ) :            
            devDocDict[dev] = list(dataDev[COMBINED_DOC_COL])

    return devDocDict

def create_document_for_Query(dataABA) :    
    data = create_data_and_combine_column(dataABA)
    logger.info("query set = " + str(len(data)))  
    
    queryList = list(data[COMBINED_DOC_COL])
    queryIdList = list(data[dataABA.docIdColName])    

    return queryIdList, queryList
    

