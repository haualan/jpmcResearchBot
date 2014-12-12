from __future__ import division
import operator,math
import nltk
import string
import os, sys
from os import sys, path
# need to add path so we can access parent folder for DB settings
# sys.path.append('../')
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import codecs
import DB
from random import shuffle
from nltk.corpus import wordnet as wn
from nltk.stem.porter import *
from nltk.stem.lancaster import LancasterStemmer
import sample



from config import KEYWORDS_NUM

docs_list = []

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def isPunct(word):
    return len(word) == 1 and word in string.punctuation

def isNumeric(word):
    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False

class keywordExtractor:
    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words())
        self.top_fraction = 1 # consider top third candidate keywords by score

    def _generate_candidate_keywords(self, sentences):
        phrase_list = []
        for sentence in sentences:
            words = map(lambda x: "|" if x in self.stopwords else x,
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

    def _generate_word_list(self,sentences):
        phrase_list = self._generate_candidate_keywords(sentences)
        word_list = []
        for i, phrase in enumerate(phrase_list):
            word_list.extend(phrase)
        return word_list

    def _calculate_word_scores(self, phrase_list):

        word_freq = nltk.FreqDist()
        for phrase in phrase_list:
            for word in phrase:
                if not isNumeric(word) and len(word)>1:
                    word_freq[wn.morphy(word)] += 1
        
        word_scores = {}
        uniqTerms = word_freq.keys()

        con = DB.get_con()

        for word in uniqTerms:
            word_scores[word] = self._calculate_tf_idf(word,word_freq,con)
        return word_scores

    def _calculate_tf_idf(self,word,word_freq,con):
        idf = DB.get_idf(word,con)
        tf = 1 + math.log(word_freq[word]) if word_freq[word] else 0
        return tf*idf
       
    def extract(self, text, incl_scores=False):
        text +=  "." if not text[-1] == "." else None
        sentences = nltk.sent_tokenize(text)
        phrase_list = self._generate_candidate_keywords(sentences)
        word_scores = self._calculate_word_scores( phrase_list)
        sorted_phrase_scores = sorted(word_scores.iteritems(),key=operator.itemgetter(1),reverse = True)#variable name should be sorted_word_scores
        sorted_phrase_scores = sorted_phrase_scores[:KEYWORDS_NUM]
        #phrase_scores = self._calculate_phrase_scores(
        #    phrase_list, word_scores)
        #sorted_phrase_scores = sorted(phrase_scores.iteritems(),
        #    key=operator.itemgetter(1), reverse=True)
        n_phrases = len(sorted_phrase_scores)
        if incl_scores:
            return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]
        else:
            return map(lambda x: x[0],
                sorted_phrase_scores[0:int(n_phrases/self.top_fraction)])

def test():
    global docs_list
    docs_list = []
    os.chdir('./txtAssets')
    for file in os.listdir("./"):
        if file.endswith(".txt"):
            docs_list.append(file)

    print 'All files: ',docs_list

    ke = keywordExtractor()

    for i,d in enumerate(docs_list):
        fileInProcessing = d
        print '\nProcessing...Extracting Keywords From...',fileInProcessing
        with open(fileInProcessing, 'r') as file:
            doc = file.read().lower()
            # doc = unicode(doc , errors='ignore')
            keywords = ke.extract( doc, incl_scores = True)
            for k in keywords:
                print k
            file.close()

def findTFIDFkeywords(istr):
    ke = keywordExtractor()
    return ke.extract(istr,incl_scores=False)
    
if __name__ == "__main__":
    # test()
    # string_a = "andy alan jpmc limited research bot maker limited process "
    string_a = sample.sample_text
    ke = keywordExtractor()
    res = ke.extract(string_a,incl_scores=False)
    print res
    print len(res)

