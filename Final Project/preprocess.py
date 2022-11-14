import re
import os
import sys
import math
import random
from stem import PorterStemmer
random.seed(28)

def removeSGML(x: str) -> str:
    pattern = re.compile(r'<.*?>')
    x = re.sub(pattern, '', x)
    return x

# expand
def abbreviation(x: str) -> str:
    x = re.sub(r'\'s', ' \'s', x)               # Jack's => Jack is
    x = re.sub(r'\'ve', ' have', x)             # I've   => I have
    x = re.sub(r'\'t', ' not', x)               # isn't  => is not
    x = re.sub(r'\'re', ' are', x)              # you're => you are
    x = re.sub(r'\'d', ' would', x)             # I'd    => I would    # or had perhaps
    x = re.sub(r'\'ll', ' will', x)             # I'll   => I will
    x = re.sub(r'\'m', ' am', x)                # I'm    => I am
    x = re.sub(r's\'', 's \'', x)               # nations' => nations '
    return x

def punctuation(x: str, lower=False) -> str:
    r = "[_.!+-=——,$%^，。？、~@#￥%……&*《》<>「」{}【】()/]–°--&”"
    
    x = re.sub(r, '', x)
    x = re.sub(r'"', '', x)
    x = re.sub(r"'", '', x)
    x = re.sub(r'\.', ' . ', x)                 # .
    x = re.sub(r',', ' , ', x)                  # ,
    x = re.sub(r'!', ' ! ', x)                  # !
    x = re.sub(r'\(', ' ( ', x)                 # (
    x = re.sub(r'\)', ' ) ', x)                 # )
    x = re.sub(r'\?', ' ? ', x)                 # ?
    x = re.sub(r'\s{2,}', ' ', x)               # multi-blank
    x = x.lower() if lower else x
    return x

def acronym(x: str) -> str:
    x = re.sub(r'(?<!\w)([A-Z])\.', r'\1', x)        # U.S.A      => USA
    x = re.sub('[^\w\s](?=\d)', '-', x)              # 01/22/2021 => 01-22-2021
    return x

def tokenizeText(x: str) -> list:
    x = x.lower()
    x = acronym(x)
    x = abbreviation(x)
    x = punctuation(x)
    return x.split()


def removeStopwords(l: list) -> list:
    # from stopwords.dms
    stopwords = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by',
                'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i',
                'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our',
                'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to',
                'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with',
                'you', 'your', '.', ',', '!', '?', ':', '(', ')', 'b', 'c', 'd', 'e', 'f', 'g',
                 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                 'x', 'y', 'z']

    # with open('stopwords.txt', 'r') as f:
    #     stopwords = [line.strip() for line in f.readlines()]

    for stopword in stopwords:
        while stopword in l:
            l.remove(stopword)
    return l

def stemWords(l: list) -> list:
    L = []
    p = PorterStemmer()
    for word in l:
        output = p.stem(word, 0, len(word)-1)
        L.append(output)
    return L

def process(path):
    wordbags = []
    wordbag = []
    w1 = w2 = []
    cnt = 0
    for i, j, k in os.walk(path):
        for file in k:
            with open(os.path.join(path, file), 'r') as f:
                s = ''.join(f.readlines())
                s = removeSGML(s)
                s = tokenizeText(s)
                s = removeStopwords(s)
                s = stemWords(s)
                wordbag.extend(s)
                wordbags.append(s)
                cnt += 1
                w1 = s if random.random() < 1 / cnt else w1
                w2 = s if random.random() < 1 / cnt else w2

    dictionary = {}
    for key in wordbag:
        dictionary[key] = dictionary.get(key, 0) + 1
    vocabulary = sorted(dictionary.items(), key=lambda item:item[1], reverse=True)

    with open('preprocess.output', 'w') as f:
        f.write(f'Words {len(wordbag)}\n')
        f.write(f'Vocabulary {len(vocabulary)}\n')
        f.write('Top 50 words\n')
        i = 0
        for v in vocabulary:
            i += 1
            if i == 50:
                break
            f.write(f'{v[0]} {v[1]}\n')

    with open('preprocess.answers', 'w') as f:
        f.write(f'1. Total number of words in the Cranfield collection is {len(wordbag)}\n')
        f.write(f'2. Vocabulary size of the Cranfield collection is {len(vocabulary)}\n')
        cnt = 0
        sum = 0
        for v in vocabulary:
            sum += v[1]
            cnt += 1
            if sum >= len(wordbag) * 0.25:
                break
        f.write(f'3. The minimum number of unique words in the Cranfield collection accounting for 25% of the total number of words in the collection is {cnt}\n')

        # v = k * n ^ b
        # v1 = k * n1 ^ b
        # v2 = k * n2 ^ b
        # b = log_(n1/n2)(v1/v2)
        # k = v1/(n1^b)

        r1 = random.randint(0, len(wordbags)-1)
        r2 = random.randint(0, len(wordbags)-1)

        w1 = wordbags[r1]
        w2 = wordbags[r2]

        f.write(f'4. Randomly pick two subsets: {r1}th file and {r2}th file.\n')

        d1, d2 = {}, {}

        for key in w1:
            d1[key] = d1.get(key, 0) + 1
        for key in w2:
            d2[key] = d2.get(key, 0) + 1
        n1, n2 = float(len(w1)), float(len(w2))
        v1, v2 = float(len(d1)), float(len(d2))
        f.write(f'Which has the property of (n, v) is ({n1}, {v1}), ({n2}, {v2})\n')
        f.write(f'According to v = k * n ^ b, \n')
        a = [1e6, 1e8]
        if v1 != v2 and n1 != n2:
            b = math.log(v1/v2, n1/n2)
            k = v1 / pow(n1, b)
            f.write('b = %.2f, k = %.2f\n' % (b, k))
            for i in a:
                f.write('When n = %d, v = %d\n' % (i, k * pow(i, b)))



if __name__ == '__main__':
    assert len(sys.argv) == 2
    root = sys.argv[1]
    # root = "cranfieldDocs/"
    process(root)