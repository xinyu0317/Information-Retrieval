from string import punctuation, ascii_uppercase, digits
import sys
from glob import glob
import os
import math
from functools import reduce
from collections import defaultdict
from tqdm import tqdm


def tokenizeText(inp):
    tokens = []
    for word in inp.split():
        if "." in word:
            if not any([x in word for x in ascii_uppercase]):
                word = word.replace(".", " ").strip()
        elif "," in word:
            if not any([x in word for x in digits]) or "," == word[-1]:
                word = word.replace(",", " ").strip()
        elif "/" in word:
            if not any([x in word for x in digits]):
                word = word.replace("/", " ").strip()
        elif "'" in word:
            if "'s" in word:
                word = word.replace("'s", " 's")
            elif "'m" in word:
                word = word.replace("I'm", "I am")
            else:
                word = word.replace("'", " ").strip()
        elif "-" in word:
            pass
        elif any([x in word for x in punctuation]):
            for c in punctuation:
                if c in word:
                    word = word.replace(f"{c}", f" ").strip()

        tokens.extend(word.split())
    return tokens


def trainNaiveBayes(train_files):
    cls_num = defaultdict(int)
    cls_prob_log = defaultdict(float)
    word_num = defaultdict(lambda: defaultdict(int))
    word_prob_log = defaultdict(lambda: defaultdict(float))

    tokenize_docs = []
    labels = []
    total_vocabulary_size = 0

    for file in train_files:
        if "true" in file:
            labels.append(1)
        elif "fake" in file:
            labels.append(0)

        token = tokenizeText(open(file, "r", encoding="utf-8").read())
        tokenize_docs.append(token)

    for i in range(len(tokenize_docs)):
        token = tokenize_docs[i]
        label = labels[i]
        cls_num[label] += len(token)
        total_vocabulary_size += len(token)
        for word in token:
            word_num[label][word] += 1

    class_num = len(set(labels))
    for label in range(class_num):
        cls_prob_log[label] = math.log(cls_num[label] / total_vocabulary_size)

    tokenize_docs_set = [set(x) for x in tokenize_docs]
    vocabulary = reduce(lambda x, y: x | y, tokenize_docs_set)

    for label in range(len(cls_num)):

        for word in vocabulary:
            word_prob_log[label][word] = math.log((word_num[label][word] + 1) / (cls_num[label] + len(vocabulary)))

    return cls_prob_log, word_prob_log, vocabulary


def testNaiveBayes(test_file, cls_prob_log, word_prob_log, vocabulary):
    token = [x for x in tokenizeText(open(test_file, "r", encoding="utf-8").read()) if x in vocabulary]
    cls_prob = []

    for label in cls_prob_log.keys():
        prob = cls_prob_log[label]
        for word in token:
            prob += word_prob_log[label][word]

        cls_prob.append(prob)

    if cls_prob.index(max(cls_prob)) == 0:
        return "fake"
    else:
        return "true"


def main(dataset):
    files = glob(dataset + "/*.txt")

    predicts = []
    for i in tqdm(range(len(files))):
        train_files = files[:i] + files[i+1:]
        test_file = files[i]
        cls_prob_log, word_prob_log, vocabulary = trainNaiveBayes(train_files)
        predict = testNaiveBayes(test_file, cls_prob_log, word_prob_log, vocabulary)
        predicts.append(predict)

    with open(f"naivebayes.output.{dataset}", "w", encoding="utf-8") as f:
        correct = 0
        for i in range(len(files)):
            f.write(os.path.basename(files[i]) + "\t" + predicts[i] + "\n")
            if predicts[i] in os.path.basename(files[i]):
                correct += 1

    print("accuracy_score: ", correct / len(files))

    print("Fake Top 10 words:")
    for word in sorted(word_prob_log[0].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(word)

    print("True Top 10 words:")
    for word in sorted(word_prob_log[1].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(word)


if __name__ == '__main__':
    main(sys.argv[1])
