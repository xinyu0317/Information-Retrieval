import sys
import os
import re
from glob import glob
from string import punctuation, ascii_uppercase, digits
from collections import Counter
from scipy.optimize import least_squares
from porter_sremmer import PorterStemmer


def removeSGML(inp):
    # return inp.split('<TEXT>')[-1].split('</TEXT>')[0]
    return " ".join(re.compile(r"<.+?>").sub("", inp).split())


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


def removeStopwords(tokens: list):
    with open("stopwords", "r") as f:
        stopwords = f.read().split()

    for i in range(len(tokens)-1, -1, -1):
        # if tokens[i] in stopwords or not d.check(tokens[i]):
        if tokens[i] in stopwords:
            tokens.pop(i)

    return tokens


def stemWords(tokens):
    p = PorterStemmer()
    stem_words = []
    for word in tokens:
        stem_words.append(p.stem(word, 0, len(word)-1))

    return stem_words


def heaps(x0, v1, v2, n1, n2):
    k, b = x0
    return [k * (n1 ** b) - v1, k * (n2 ** b) - v2]


def main(dirname):
    total_words = []
    subsets = []
    for file in glob(os.path.join(dirname, "*")):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            content = removeSGML(content)
            tokens = tokenizeText(content)
            tokens = removeStopwords(tokens)
            stem_tokens = stemWords(tokens)
            total_words.extend(stem_tokens)
            subsets.append(stem_tokens)

    sorted_words = sorted(Counter(total_words).items(), key=lambda x: x[1], reverse=True)
    with open("preprocess.output", "w", encoding="utf-8") as f:
        f.write(f"Words {len(total_words)}\n")
        f.write(f"Vocabulary {len(set(total_words))}\n")
        f.write("Top 50 words\n")
        for word, count in sorted_words[:50]:
            f.write(f"{word} {count}\n")

    with open("preprocess.answers", "w", encoding="utf-8") as f:
        f.write(f"Cranfield's total collection is {len(total_words)} words.\n")
        f.write(f"Cranfield's collection of words is {len(set(total_words))}.\n")

        value = len(total_words) * 0.25
        number = 0
        for word, count in sorted_words:
            value -= count
            number += 1
            if value <= 0:
                break

        f.write(f"{number} word accounts for 25% of the total {len(total_words)} words.\n")

        v1, v2, n1, n2 = (len(set(subsets[0])), len(set(subsets[1])), len(subsets[0]), len(subsets[1]))
        k, b = least_squares(heaps, [0, 0], args=(v1, v2, n1, n2)).x

        f.write(f"– For {len(subsets[0])} words, there are {len(set(subsets[0]))} unique words.\n")
        f.write(f"– For {len(subsets[1])} words, there are {len(set(subsets[1]))} unique words.\n")

        # print(k, b)
        f.write(f"The corpus is increased to 1,000,000 with a vocabulary of {int((1000000 / k) **(1/b))}\n")
        f.write(f"The corpus is increased to 100,000,000 with a vocabulary of {int((100000000 / k) **(1/b))}\n")


if __name__ == '__main__':
    main(sys.argv[1])

    # main(".\cranfieldDocs")
