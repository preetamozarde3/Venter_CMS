# -*- coding: utf-8 -*-
"""
Created on Tue June 25 2019

@author: Anushri Arora
"""

import os
import re

import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize

from Backend.settings import BASE_DIR


def parse(filepath, domain_present, domain_keyword_dict_keys):
    '''
    This function parses the fed csv file and saves them separately,
    segregating the categories
    Args(1) - csv filepath
    '''
    final_domain_names = []

    if domain_present:
        print("DOMAINS are PRESENT IN input file")
        xls = pd.ExcelFile(filepath)
        df = pd.read_excel(xls, 'Form responses 1', header=[0, 1])

        headers = df.keys()[1:]
        headers = headers[:len(headers)-3]
        
        for h in headers[1::2]:
            filename = str(h).split(',')[0].split('\'')[1] + '.txt'
            domain_name = filename[:-4]
            domain_name = domain_name.lower()
            
            if domain_name in domain_keyword_dict_keys:
                print("header name from file that also exists in db domain_keyword_dict: ", domain_name)
                print("inside IF LOOP OF PARSE function")
                print("the filename to be created for the domain is: ", filename)
                file = open(os.path.join(BASE_DIR, 'Venter/ML_model/Civis/data/keyword data/') + filename, 'w', encoding='utf-8')
                index = 1
                print("Parsing " + filename + '...')
                for sentence in df[h]:
                    if type(sentence) == str:
                        file.write(str(index) + '- ' + sentence.lstrip().replace('\n', ' ') + '\n')
                        index += 1
                final_domain_names.append(domain_name)
        print("final_domain_names list in IF PART of csv parser-----------------------")             
        print(final_domain_names)
    else:
        print("NO DOMAINS PRESENT IN input file++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        raw_data = pd.read_excel(filepath, skiprows=1)
        print("type of RAWDATA ------------------: ", type(raw_data))
        response = raw_data['Feedback']
        print("type of response contaning FEEDBACK column: ", type(response))
        response=response.dropna()
        print("type of response after DROPNA: ", type(response))
        response = response.to_frame()
        print("type of response after converting into PANDAS FRAME: ", type(response))

        print("Null values are: ", response.isnull().sum())

        domain_keyword_dict_keys = list(domain_keyword_dict_keys)
        domain_name=domain_keyword_dict_keys[0]
        final_domain_names.append(domain_name)

        tokenized_text=[]
        num=1
        for index, row in response.iterrows():
            data = row[0]
            tokenized_text+=sent_tokenize(data)
        my_df = pd.DataFrame(tokenized_text)

        name = domain_name+'.txt'
        path = 'Venter/ML_model/Civis/data/keyword data/'+name
        my_df.to_csv(path, index=None, header=None, sep = ' ', mode='a')
        print("final_domain_names list in ELSE PART of csv parser-----------------------")
        print(final_domain_names)

    return final_domain_names    
