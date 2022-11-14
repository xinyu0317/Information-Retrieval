import sys
import os
import re
import numpy as np
from preprocess import *


class vector_space_class:

    # The inverted index with the following structure
    # {token: [df, {doc_ID: tf, doc_ID: tf, ...}],
    #   token: [df, {doc_ID: tf, doc_ID: tf, ...}],...}
    inverted_index = dict()
    #pair of documents and their vocabulary number
    doc_num_voca = dict()                 

    def process_index(self, doc_ID, word_list):
        self.doc_num_voca[doc_ID] = len(word_list)
        for token in word_list:
            #Default the dicts
            default_value = [0,dict()]
            self.inverted_index.setdefault(token,default_value)
            self.inverted_index[token][1].setdefault(doc_ID,0)

            #Update interted matrix
            self.inverted_index[token][1][doc_ID] += 1
            self.inverted_index[token][0] = len(self.inverted_index[token][1].keys())
        return


    def doc_matrix(self, doc_weighting_name):
        #Try [t][xfp][cx]
        docs = len(self.doc_num_voca.keys())+1
        tokens = len(self.inverted_index.keys())
        d_matrix = np.ones((docs,tokens),dtype=np.float32)

        for doc in range(docs):
            token_num = 0
            for token in self.inverted_index.keys():
                tfc = 1.0
                df, doc_dict = self.inverted_index[token]
                # tfc               
                if doc not in doc_dict.keys():
                    tfc = 0
                else:
                    tfc = doc_dict[doc]
                # cfc
                cfc = 1.0
                df = self.inverted_index[token][0]
                if doc_weighting_name[1] == 'x':
                    cfc = 1.0
                elif doc_weighting_name[1] == 'f':
                    cfc = np.log(len(self.doc_num_voca.keys())/df)
                elif doc_weighting_name[1] == 'p':
                    cfc = np.log((len(self.doc_num_voca.keys())-df)/df)
                d_matrix[doc][token_num] = tfc * cfc
                token_num += 1

        if doc_weighting_name[2] == 'c':
            d_matrix /= (np.linalg.norm(d_matrix, axis=1).reshape(-1,1)+0.1)

        return d_matrix[1:]


    def query_matrix(self, que_weighting_name, query_tokens):

        query_dict = dict()
        for token in query_tokens:
            query_dict.setdefault(token,0)
            query_dict[token] += 1
        tokens = len(self.inverted_index.keys())
        
        #Try [t][xfp][cx]
        q_matrix = np.ones((tokens,1),dtype=np.float32)
        token_num = 0
        for token in self.inverted_index.keys():
            # tfc
            tfc = 1.0
            if token not in query_dict.keys():
                tfc = 0
            else:
                tfc = query_dict[token]
            
            # cfc
            cfc = 1.0
            df = self.inverted_index[token][0]
            if que_weighting_name[1] == 'x':
                cfc = 1.0
            elif que_weighting_name[1] == 'f':
                cfc = np.log(len(self.doc_num_voca.keys())/(df))
            elif que_weighting_name[1] == 'p':
                cfc = np.log((len(self.doc_num_voca.keys())-df)/(df))
            q_matrix[token_num] = tfc * cfc
            token_num += 1

        if que_weighting_name[2] == 'c':
            q_matrix /= (np.linalg.norm(q_matrix, axis=1).reshape(-1, 1) + 0.1)
        return q_matrix


    def __init__(self):
        self.inverted_index = dict()
        self.doc_num_voca = dict()
    
    

class train_class():

    doc_weighting_name = "tfc"
    que_weighting_name = "tfx"

    def indexDocument(self,doc_ID, word_list,inverted_index: vector_space_class):
        inverted_index.process_index(doc_ID, word_list)
        return inverted_index

    def retrieveDocuments(self, query_tokens, inverted_index: vector_space_class, que_weighting_name, weighting_matrix):
        query_weight = inverted_index.query_matrix(que_weighting_name, query_tokens)
        similar_array = np.matmul(weighting_matrix,query_weight) / (np.linalg.norm(weighting_matrix, axis=1).reshape(-1, 1) *\
             np.linalg.norm(query_weight).reshape(-1, 1))
        return similar_array
    
    def train_model(self):
        #main_fold should named train_data
        main_folder = "train_data/"
        #each city has a folder named the city's name
        cities_folder_list = os.listdir(main_folder)

        # output
        output_filename = "training_result.output"
        out_file = open(output_filename, 'w')

        header = 'city\tbest season\tbest_score\n'
        out_file.write(header)
        for city in cities_folder_list:
            if city in('.DS_Store', '.localized'):
                continue
            path = main_folder+city
            reviews_doc = os.listdir(path)
            print("finding best season for " + city + '\n')

            doc_ID = 0
            doc_vectorspace = vector_space_class()
            for review in reviews_doc:
                if review not in ('.DS_Store', '.localized'):
                    doc_ID += 1
                    file_path = path + '/'+ review
                    with open(file_path, 'r') as f:
                        sentence = ' '.join(f.readlines())
                    review_word_list = removeStopwords(tokenizeText(sentence))
                    self.indexDocument(doc_ID, review_word_list, doc_vectorspace)

            doc_martix = doc_vectorspace.doc_matrix(self.doc_weighting_name)
            query_file_name = 'season_queries.output'
            query_file = open(query_file_name)
            best_score = 0
            for query in query_file.readlines():
                query_tokens  = []
                query_tokens = removeStopwords(tokenizeText(query))
                query_name = query_tokens[0]
                query_tokens = query_tokens[1:]
                similarity_docs = self.retrieveDocuments(query_tokens,doc_vectorspace,self.que_weighting_name, doc_martix)
                sum_score = np.sum(similarity_docs)
                if sum_score > best_score:
                    best_score = sum_score
                    best_season = query_name
            # output the result
            result = city + '\t' + best_season + '\t' + str(best_score) + '\n'
            out_file.write(result)

        def __init__(self):
            self.doc_weighting_name = "tfc"
            self.que_weighting_name = "tfx" 



if __name__ == '__main__':

    training = train_class()
    training.train_model()

