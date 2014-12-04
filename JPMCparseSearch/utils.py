import math
import numpy as np
# decision tree stuff
# trying to feed in word frequency data to determine whether review is positive or negative

# Suppose we want ID3 to decide whether the review is positive or negative. 
# The target classification is "is this a positive review" which can be yes or no.

# The attributes are occurences of the top 30 words. We will not consider the count of words otherwise we overcomplicate the model by creating too many nodes
# if the certain word appears, the attribute is 1 otherwise it's 0



def entropy(iData):
#iData is a list of 0 and 1 like: [0,1,1,0,0...], if it's 0 it's negative (absensce of word), 1 if positive (presence of word)
    

    pos = float(sum(iData))
    l = float(len(iData))
    neg = float(l - pos)

    if pos == 0 or neg == 0 :
        # a math domain error would occur if there is complete order, as in all items in the list are the same
        r = 0.0
    else:
        r = (- (pos/l) * math.log((pos/l),2)) + (-(neg/l) * math.log((neg/l),2))


    return r

def information_gain(x):
# note here iData must contain the full table of all attributes. Passing only 1 variable to function so I can use pool.map multiprocessing
    
    iData = x[0]
    iAttributeColumn = x[1]

    ent = entropy(iData[:,0])
    pos_attrib = float(sum(iData[:,iAttributeColumn]))
    l_attrib = float(len(iData[:,iAttributeColumn]))
    neg_attrib = float(l_attrib - pos_attrib)

    # print ent, pos_attrib, l_attrib, neg_attrib
    pos_within_attrib = iData[ (iData[0::,iAttributeColumn] == '1' or iData[0::,iAttributeColumn] == 1),0]
    neg_within_attrib = iData[ (iData[0::,iAttributeColumn] == '0' or iData[0::,iAttributeColumn] == 0),0]


    r = ent + (-(pos_attrib/l_attrib) * entropy(pos_within_attrib)) + (-(neg_attrib/l_attrib) * entropy(neg_within_attrib))


    return (iAttributeColumn,r)

# natural language processing stuff
def freq(lst):
    freq = {}
    length = len(lst)
    for ele in lst:
        if ele not in freq:
            freq[ele] = 0
        freq[ele] += 1
    return (freq, length)

def get_unigram(review):
    return freq(review.split())

def get_unigram_list(review):
    return get_unigram(review)[0].keys()

# need to implement a custom_get_unigram function (in utils.py) because 
# 1. I need to preserve the target classification (good/bad review) during the mapping process
# 2. Handle the filtering of the words we only want to produce a list that represents the presence and absense of those UNION SET of words

def custom_get_unigram(iData):
  # words = iData[2]  
  unigram_lst = get_unigram_list(iData[0])


  r = [int(iData[1])]
  r.append( unigram_lst)

  return r


