import nltk
import os
from query_search import query_finding
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup
import re

query = query_finding() 

def doctors_fill(doctors, data):
    for i in range(0, len(data)):     
        doctors.append([None])
        for j in range(0, 15):
            if(j % 2 != 0):
                doctors[i].append(data[i][j])
        doctors[i].pop(0)
    return doctors        



def dictionary_fill(dictionary, doctors, cities, specialities):
    for i in range(0, 100):
        dictionary.update({cities[i].lower(): []})

    for i in range(0, 4):
        dictionary.update({specialities[i]: []})
        
    for i in range(0, len(doctors)):
        dictionary[doctors[i][6]].append(i)
        dictionary[doctors[i][2]].append(i)
    return dictionary    
        

def main_query_fill(main_query):
    words = word_tokenize(query.lower())  
    stop_words = set(stopwords.words('english'))
        
    for word in words:
        if word not in stop_words:
            main_query.append(word)      
    return main_query        
          








