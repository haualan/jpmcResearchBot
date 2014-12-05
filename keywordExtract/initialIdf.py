from __future__ import division
import operator
import nltk
import string
import os
import codecs
from random import shuffle
from nltk.corpus import wordnet as wn
from nltk.stem.porter import *
from nltk.stem.lancaster import LancasterStemmer
import mysqlHandler
from config import DOC_DIRECTORY

docs_list = []

def isPunct(word):
    return len(word) == 1 and word in string.punctuation

def isNumeric(word):
    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False
    
def _getSources():
    all_word_lists = []
    for i,f in enumerate(docs_list):
        with open(f, 'r') as file:
            text = file.read().lower()
            text = unicode(text , errors='ignore')
            sentences = nltk.sent_tokenize(text)
            #print self._generate_word_list(sentences)
            current_doc_uniq_word_list = list(set(_generate_word_list(sentences)))
            
            con = mysqlHandler.get_con()

            for w in current_doc_uniq_word_list:
                if not isNumeric(w) and len(w)>1:
                    mysqlHandler.incr_occurrence(w,con)
            mysqlHandler.incr_total_doc_number(con)

            con.close()
            file.close()

    return all_word_lists

def _generate_word_list(sentences):
    phrase_list = _generate_candidate_keywords(sentences)
    word_list = []
    for i, phrase in enumerate(phrase_list):
        word_list.extend(phrase)
    return word_list

def _generate_candidate_keywords(sentences):
    phrase_list = []
    stopwords = set(nltk.corpus.stopwords.words())
    for sentence in sentences:
        words = map(lambda x: "|" if x in stopwords else x,
            nltk.word_tokenize(sentence.lower()))
        phrase = []
        for word in words:
            if word == "|" or isPunct(word):
                if len(phrase) > 0:
                    phrase_list.append(phrase)
                    phrase = []
            else:
                word = wn.morphy(word)
                phrase.append(word) if word else None
                #stemmer = PorterStemmer()
                #print 'word:::',word
                #stemmed_word = stemmer.stem(word)
                #print 'stemmed_word:::',stemmed_word
                #phrase.append(stemmed_word)
                #phrase.append(word)
    return phrase_list


def test():
    global docs_list
    os.chdir(DOC_DIRECTORY)
    for file in os.listdir("./"):
        if file.endswith(".txt"):
            docs_list.append(file)

    print 'All files: ',docs_list

    print _getSources()

if __name__ == "__main__":
    test()
