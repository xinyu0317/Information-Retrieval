import os
import sys
from tqdm import tqdm
from collections import Counter
from glob import glob
from itertools import chain
from preprocess import removeSGML, tokenizeText, removeStopwords, stemWords
import numpy as np
# from numpy import dot
# from numpy.linalg import norm


def parse_text(text):
    content = removeSGML(text)
    tokens = tokenizeText(content)
    tokens = removeStopwords(tokens)
    tokens = stemWords(tokens)
    return tokens


def indexDocument(doc, ws, wq):
    item = dict()
    tokens = parse_text(doc)
    item["t"] = dict(Counter(tokens))
    item["ws"] = ws
    item["wq"] = wq
    return item


def parse_vec(t, wm):
    vec = np.zeros(len(words))

    for w in t.keys():
        if w in words:
            i = words.index(w)
            if wm == "tfx" or wm == "tfc":
                vec[i] = t[w] * np.log10(N / n[w])
            elif wm == "nxx":
                vec[i] = (0.5 * t[w]) / max(t.values())
            elif wm == "bpx":
                vec[i] = np.log10((N - n[w]) / n[w])
            else:
                raise

    if wm == "tfc":
        vec = vec * 1/np.sum(np.sqrt(np.power(vec, 2)))
    elif wm == "nxx":
        vec = vec + 0.5

    return vec


def parse_query_vec(query, wq):
    query_tokens = parse_text(query)
    t = dict(Counter(query_tokens))
    query_vec = parse_vec(t, wq)
    return query_vec


def cosine_similarity(v1, v2):
    return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


def retrieveDocuments(query, documents, ws, wq):
 
    query_vec = parse_query_vec(query, wq)

    ids_cos = []

    for doc_id in documents:
        sim = cosine_similarity(documents[doc_id]["vec"], query_vec)
    
        ids_cos.append([doc_id, sim])

    return ids_cos


def read_output(file):
    with open(file, "r") as f:
        query_docs = dict()
        for line in f.readlines():
            query_id = line.split()[0]
            doc_id = line.split()[1]
            if query_id in query_docs:
                query_docs[query_id].append(doc_id)
            else:
                query_docs[query_id] = [doc_id]

    return query_docs



def calculate_precision_recall(pre, answer):
    precision = []
    recall = []

    for doc_num in [10, 50, 100, 500]:
        _precision = []
        _recall = []
        for query_id in pre:
            pre_id = set(pre[query_id][:doc_num])
            answer_id = set(answer[query_id][:doc_num])
            w = len(pre_id & answer_id)
            x = len(answer_id - pre_id)
            y = len(pre_id - answer_id)

            _recall.append(w / (w + x))
            _precision.append(w / (w + y))

        precision.append(np.mean(_precision))
        recall.append(np.mean(_recall))

    return precision, recall


def main(ws, wq, dirname, q_file):
    global n, N, words
    documents = dict()
    # for file in glob(os.path.join(dirname, "*")):
    for file in tqdm(glob(os.path.join(dirname, "*"))):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            item = indexDocument(content, ws, wq)
            documents[int(file[-4:])] = item

    n = dict(Counter(list(chain(*[list(x["t"].keys()) for x in documents.values()]))))
    N = len(documents)
    words = list(n.keys())

    for i in documents:
        documents[i]["vec"] = parse_vec(documents[i]["t"], ws)

    # output
    with open(f"cranfield.{ws}.{wq}.output", "w") as output_file:
        with open(q_file, "r") as f:
            queries = f.readlines()
            for query_line in tqdm(queries):
                query_id = int(query_line.split()[0])
                query = " ".join(query_line.split()[1:])
                ids_cos = retrieveDocuments(query, documents, ws, wq)

                for doc_id, score in sorted(ids_cos, key=lambda x: x[1], reverse=True):
                    output_file.write(f"{query_id} {doc_id} {score}\n")

    # answer
    reljude = read_output("cranfield.reljudge")

    with open("cranfield.answer", "w") as answer:
        answer.write(f"My weighting scheme is nxx.bpx.\n")
        answer.write(f"The length of the query string is not long, I think this is the best probability weight, "
                f"it should be effective\n\n")

        doc_nums = [10, 50, 100, 500]
        for file in ["cranfield.tfc.tfx.output", "cranfield.nxx.bpx.output"]:
            if os.path.exists(file):
                pre = read_output(file)
                precision, recall = calculate_precision_recall(pre, reljude)

                answer.write("\n"+file+"\n")
                for i in range(len(precision)):
                    answer.write(f"Top {doc_nums[i]} precision: {precision[i]:.4f} recall: {recall[i]:.4f}\n")


if __name__ == '__main__':
    global n, N, words

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    # main("tfc", "tfx", "cranfieldDocs/", "cranfield.queries")
    # main("nxx", "bpx", "cranfieldDocs/", "cranfield.queries")
