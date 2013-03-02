#!/usr/bin/python2.7

import nltk
import re
import tokenize

from nltk.corpus import stopwords

def gen_words(sources):
    for line in sources:
        for w in line.split():
            yield w

#texts = open('/home/ko/nltk_data/corpora/genesis/lolcat.txt')
texts = open('/home/ko/nltk_data/corpora/genesis/english-kjv.txt')
text = gen_words(texts)

stopwords=nltk.corpus.stopwords.words('english') 

track = [word for word in text if word not in stopwords]
remove_punctuation = re.compile('.*[A-Za-z0-9].*')

filtered = [word for word in track if remove_punctuation.match(word)]

freq_distribution = nltk.FreqDist(filtered)

freq_count = freq_distribution.items()

print freq_count[:50]
