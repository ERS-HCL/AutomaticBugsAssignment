# -*- coding: utf-8 -*-
"""
@author: ashwinkumars
"""

from __future__ import division

import math
import re
import string
import operator

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import logging

logger = logging.getLogger(__name__)

def tokenize(doc) :
    return doc.lower().split(" ")

def tokenize_set(allDocuments) :    
    tokenizedDocuments = [tokenize(d) for d in allDocuments] # tokenized docs
    
    return set([item for sublist in tokenizedDocuments for item in sublist])   

def sanitize_doc(doc) :
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()    
    
    if doc != doc : #check for NaN
        doc = ''
    else :        
        doc = ''.join(ch for ch in doc if ch not in exclude)
        doc = ' '.join(lemma.lemmatize(word) for word in doc.split())
        doc = ' '.join([i for i in doc.lower().split() if i not in stop])          
        #doc = re.sub("[^a-zA-Z0-9 ]", "", doc)        
        doc = doc.strip()        
        
    return doc    

def sanitize_docs(allDocuments) :   
    sanitizeDocs = []
    
    for doc in allDocuments :
        doc = sanitize_doc(doc)        
        if doc == '' :
            continue
        
        sanitizeDocs.append(doc) 
   
    return sanitizeDocs    

# term frequency (t,d)
def term_frequency(term, document) :       
    return document.count(term.lower())

# logarithmic term frequency = log(tf(t, d))
# using document term weight defined for weighing scheme 2
# so adding 1 to result
# source :wikipedia  (recommended TF-IDF weighing schemes )
#       
def logarithmic_term_frequency(term, document) :
    freq = term_frequency(term, document)    
   
    if(freq > 0) :
        return 1 + math.log(freq)
    else :
        return 0

# method of normalizing document length for comparison
# cos Θ = (dot product of vectors)/ ((magnitude of vector1) * (magnitude of vector2))
def cosine_similarity(vector1, vector2) :
    cSimilarity = 0
    dotProduct = sum(dimensionV1 * dimensionV2 for dimensionV1, dimensionV2 in zip(vector1, vector2))
    magnitudeVector1 = math.sqrt(sum([val**2 for val in vector1]))
    magnitudeVector2 = math.sqrt(sum([val**2 for val in vector2]))
    productMagnitude = magnitudeVector1 *  magnitudeVector2
    
    if productMagnitude != 0:
        cSimilarity = dotProduct/productMagnitude
        
    return cSimilarity

# =============================================================================
# idf(t, D) = log(N/|{d ε D : t ε T}|)
# where : 
#     N = total number of documents in the corpus.
#     |{d ε D : t ε T}| = number of documents t where the term appears .
#     1 is added as weight
# =============================================================================

def inverse_document_frequencies(tokenizeDocuments) :
    idfValues = {}    
    allTokensSet = set([item for sublist in tokenizeDocuments for item in sublist])
    for tkn in allTokensSet :        
        containsToken = map(lambda doc : tkn in doc, tokenizeDocuments)       
        sumContainsToken = sum(containsToken)
        
        if(sumContainsToken != 0) :
            idfValues[tkn] = 1 + math.log(len(tokenizeDocuments)/(sumContainsToken))
        else :
            idfValues[tkn] = 0
    
    return idfValues

# tfidf(t, d, D) = tf(t, d)*idf(t, d)
def calculate_TFIDF(idf, document) :
    docTFIDF = []
    for term in idf.keys() :
        tf = logarithmic_term_frequency(term, document)
        docTFIDF.append(tf * idf[term])
        
    return docTFIDF

def tfidf(documents) :
    tokenizedDocuments = [tokenize(d) for d in documents]   
    idf = inverse_document_frequencies(tokenizedDocuments)
    tfidfDocuments = []
    for document in tokenizedDocuments :
        tfidfDoc = calculate_TFIDF(idf, document)        
        tfidfDocuments.append(tfidfDoc)
    
    return tfidfDocuments, idf            

def algo1(allDocuments) :     
    
    return tfidf(allDocuments)

def create_cosine_similarity_matrix(vectorRepresentation) :
    tfidfComparisons = []
    
    for count0, doc0 in enumerate(vectorRepresentation) :
        for count1, doc1 in enumerate(vectorRepresentation) :
            cSimilar = cosine_similarity(doc0, doc1)           
            tfidfComparisons.append((cSimilar, count0, count1))
        
    return  tfidfComparisons

def get_max_cosine_similarity_number(vectorRepresentation, index) :
    maxNum = 0
    retIndex = 0    
    
    for count, doc0 in enumerate(vectorRepresentation) :        
        if count != index :
            cSimilar = cosine_similarity(doc0, vectorRepresentation[index])            
            if maxNum < cSimilar :
                maxNum = cSimilar
                retIndex = count                
    
    return  maxNum, retIndex

def get_max_cosine_similarity_number2(vectorRepresentationallDoc, vectorRepQuery) :
    similarityVector = []
    
    for count, doc0 in enumerate(vectorRepresentationallDoc) :        
        cSimilar = cosine_similarity(doc0, vectorRepQuery)
        similarityVector.append(cSimilar)    
    
    return  similarityVector
            
def run(allDocuments, compareIndex = 0) :
    
    tfidfRepresentation, idf = algo1(allDocuments)     
    similarityNumber, index = get_max_cosine_similarity_number(tfidfRepresentation, compareIndex)   
    
    return similarityNumber, index


def get_assigned_dev(similarityVector, devMap) :    
    maxIndex, cSimilarEstimate = max(enumerate(similarityVector), key = operator.itemgetter(1))
    
    indexCount = 0
    assignedDev = ""    
    
    for currdev, itemCount in devMap.items() :        
        indexCount = indexCount + itemCount
        if maxIndex <= (indexCount -1) and assignedDev == "" :
            assignedDev = currdev
            break         
    
    return assignedDev


def get_assigned_dev_and_delta(similarityVector, devMap, dev) :     
    #delta = 0
    maxIndex, cSimilarEstimate = max(enumerate(similarityVector), key = operator.itemgetter(1))
    #cSimilarEstimate = cSimilarEstimate - delta    
    #maxIndex = similarityVector.index(min(similarityVector, key=lambda x : abs(x - cSimilarEstimate)))
    
    indexCount = 0
    assignedDev = ""
    startDevIndex = -1
    endDevIndex = 0
    
    for currdev, itemCount in devMap.items() :        
        indexCount = indexCount + itemCount
        if maxIndex <= (indexCount -1) and assignedDev == "" :
            assignedDev = currdev            
        
        if startDevIndex == -1 and dev == currdev :
            startDevIndex = indexCount - itemCount
            endDevIndex = indexCount
            
    cSimilarExpected = max(similarityVector[startDevIndex : endDevIndex])    
    
    return assignedDev, cSimilarExpected - cSimilarEstimate


def get_similarity_vector(tfidfRepresentation, idf, query) :  
    tfidfRepresentationQuery = calculate_TFIDF(idf, query)   
    similarityVector = get_max_cosine_similarity_number2(tfidfRepresentation, tfidfRepresentationQuery)   
  
    return similarityVector

