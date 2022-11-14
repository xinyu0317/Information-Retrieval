import sys
import os
from string import punctuation
from collections import Counter
import math


def trainBigramLanguageModel(inp: str):

    words = inp.split()
    single_words = [w for w in words if w not in punctuation]
    bigram_word = [(single_words[i], single_words[i+1]) for i in range(len(single_words) - 1)]

    single_freq = dict(Counter(single_words))
    bigram_freq = dict(Counter(bigram_word))

    return single_freq, bigram_freq


def identifyLanguage(text, languages, single_freqs, bigram_freqs):
    p = []
    words = text.split()
    single_words = [w for w in words if w not in punctuation]
    for i in range(len(languages)):
        _p = 0
        for j in range(len(single_words) - 1):
            denominator = bigram_freqs[i].get((single_words[j], single_words[j+1]), 0) + 1
            numerator = single_freqs[i].get(single_words[j], 0) + len(single_freqs[i].keys())
            _p += math.log2(denominator / numerator)

        p.append(_p)

    index = sorted(range(len(p)), key=lambda k: p[k])[-1]
    return languages[index]


def main(test_file):
    dataset_dir = os.path.dirname(test_file)
    languages = os.listdir(dataset_dir + "/training")
    single_freqs = []
    bigram_freqs = []
    for language in languages:
        with open(dataset_dir + "/training/" + language, "r", encoding="utf-8", errors="ignore") as f:
            single_freq, bigram_freq = trainBigramLanguageModel(f.read())
        single_freqs.append(single_freq)
        bigram_freqs.append(bigram_freq)

    predict = []
    with open(test_file, "r", encoding="utf-8", errors="ignore") as f:
        for text in f.readlines():
            pre_lang = identifyLanguage(text, languages, single_freqs, bigram_freqs)
            predict.append(pre_lang)

    with open("languageIdentification.output", "w", encoding="utf-8") as f:
        for line, lang in enumerate(predict):
            f.write(f"{line+1} {lang}\n")

    with open(dataset_dir + "/solution", "r", encoding="utf-8") as f:
        y = [x.strip().split()[-1] for x in f.readlines()]

    with open("languageIdentification.answers", "w", encoding="utf-8") as f:
        accuracy = len([i for i in range(len(predict)) if predict[i] == y[i]]) / len(predict)
        f.write(f"The accuracy rate is {accuracy}")


if __name__ == '__main__':
    main(sys.argv[1])
