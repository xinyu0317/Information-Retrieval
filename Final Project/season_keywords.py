import os
import sys
import math
from preprocess import *


def read(file: str) -> list:
    with open(file, 'r') as f:
        sentence = ' '.join(f.readlines())
    words = tokenizeText(sentence)
    words = removeStopwords(words)
    # words = stemWords(words)
    return words


def getData(dataPath):
    Spring, Summer, Autumn, Winter = [], [], [], []
    for i, j, k in os.walk(dataPath):
        for file in k:
            if file.startswith('spring'):
                Spring.extend(read(os.path.join(i, file)))
            if file.startswith('summer'):
                Summer.extend(read(os.path.join(i, file)))
            if file.startswith('fall'):
                Autumn.extend(read(os.path.join(i, file)))
            if file.startswith('winter'):
                Winter.extend(read(os.path.join(i, file)))
    # print(Spring, Summer, Autumn, Winter)
    return Spring, Summer, Autumn, Winter

def tf_idf(articles: list):
    V = {}
    TF, IDF, TFIDF = [], [], []

    # calculate tf
    for article in articles:
        tf = {}
        for word in article:
            V[word] = V.get(word, 0) + 1
            tf[word] = tf.get(word, 0) + 1
        TF.append(tf)

    # calculate idf
    for article in articles:
        idf = {}
        for word in article:
            if idf.get(word, 0):
                continue
            count = 0
            for tf_season in TF:
                if tf_season.get(word, 0):
                    count += 1
            idf[word] = math.log(num_of_seasons / count, 2)
        IDF.append(idf)

    # calculate tf-idf
    v = list(V)
    D = []
    for i, season in enumerate(seasons):
        tfidf = []
        d = {}
        for word in v:
            n = TF[i].get(word, 0) * IDF[i].get(word, 0)
            tfidf.append(n)
            d[word] = n
        TFIDF.append(tfidf)
        D.append(d)

    return D

def get_key_words_and_tfidf(D:list, num_of_keywords: int, seasons):
    L = []
    for i, season in enumerate(seasons):
        l = sorted(D[i].items(), key=lambda item:item[1], reverse=True)
        L.append(l)
        # print(season, l[:num_of_keywords])
    return L

def get_key_words(D:list, num_of_keywords: int):
    L = []
    outputFile = 'season_queries.output'
    with open(outputFile, 'w', encoding="utf-8") as f:
        for i, season in enumerate(seasons):
            l = sorted(D[i].items(), key=lambda item:item[1], reverse=True)
            a = [x[0] for x in l]
            L.append(a)
            print(season, a[:num_of_keywords])
            f.write(str(season) + ' ')
            for word in a[:num_of_keywords]:
                f.write(str(word) + ' ')
            f.write('\n')
    return L

if __name__ == '__main__':
    num_of_seasons = 4
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    a, b, c, d = getData('season_articals')
    D = tf_idf([a, b, c, d])
    num_of_words = int(sys.argv[1])
    # get_key_words_and_tfidf(D, num_of_words)
    get_key_words(D, num_of_words)
