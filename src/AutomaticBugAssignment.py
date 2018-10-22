# -*- coding: utf-8 -*-
"""
@author: ashwinkumars
"""

import argparse
import logging

from ABAInputXMLDataProcessor import load_input_data
from ABASimulator import execute_sim
from ABATrain import execute_train_and_dump_data
from ABAQuery import execute_query

from ABAInputXMLDataProcessor import SIMULATE
from ABAInputXMLDataProcessor import TRAIN
from ABAInputXMLDataProcessor import QUERY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

    
def simulation(inputFile) :
    listABAInputs = load_input_data(inputFile, SIMULATE)
    for dataABA in listABAInputs :         
        execute_sim(dataABA) 
            
def train(inputFile) :
     listABAInputs = load_input_data(inputFile, TRAIN)
     for dataABA in listABAInputs : 
        execute_train_and_dump_data(dataABA) 

def query(inputFile) :
     listABAInputs = load_input_data(inputFile, QUERY)
     for dataABA in listABAInputs : 
         execute_query(dataABA) 

def main() :    
    logger.info('Executing AutomaticBugAssignment program.')
    
    parser = argparse.ArgumentParser(description='AutomaticBugAssignment')  
    parser.add_argument("-t", "--type", dest = "type", required = True, choices = {SIMULATE, TRAIN, QUERY})
    parser.add_argument("-f", "--file", dest = "filename", required = True, help = "Input file to read")
    args = parser.parse_args()   
    
    inputFile = args.filename
    if args.type == 'simulate' :
        simulation(inputFile)
        
    elif args.type == 'train' :
        train(inputFile)
        
    elif args.type == 'query' :
        query(inputFile)
 
    logger.info('Executing AutomaticBugAssignment program completed.')
    
if __name__== "__main__" :
    main()
