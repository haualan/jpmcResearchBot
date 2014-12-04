import nltk, re, string
from multiprocessing import Pool
import operator
import utils as ut
import numpy as np
import csv
from nltk.corpus import stopwords
from nltk import bigrams
from nltk import trigrams
from nltk.util import ngrams

# constants
BINARY = True
NONWORDS = re.compile('[\W_]+')
STOPWORDS = stopwords.words('english')

data = []
#use all cores and multiprocesses to analyze data
my_pool = Pool() 

def reduce_unigram_list_freq(lst):
  freq = {}
  for i in lst:
    # print(i[0])
    for j in i[0]:
      if j not in freq:
        freq[j] = 0
      freq[j] += i[0][j]

  return freq


def get_popular_unigrams(iReviews):
  # process every item in the reviews to get unigram, use map
  mapped_unigram_list = list(my_pool.map(ut.get_unigram, iReviews))

  # reduce the results after they are done
  final_unigram = reduce_unigram_list_freq(mapped_unigram_list)

  # sorted
  sorted_final_unigram = sorted(final_unigram.items(), key=operator.itemgetter(1), reverse=True)

  return sorted_final_unigram

with open('SEARCH_STATS_formatted.csv', 'rU') as csvfile:
  f = csv.reader(csvfile, delimiter=',')
  for row in f:
    row = (str(row)[2:-2]).strip().lower()
    if row != '':
      data.append(row)

# data = np.array(data)
data_length = len(data)
print 'number of non-blank search terms in total:', data_length

c = 0
for i in data:
  if '"' in i: c+=1
  if ' and ' in i: c+=1
  if ' or ' in i: c+=1
  if i.find(')') != -1 or i.find('(') != -1 : c+=1

print 'complex_searches', float(c)/data_length

search_lengths = {}
for i in data:
  freq = len(i.split())
  if freq not in search_lengths:
    search_lengths[freq] = 0
  search_lengths[freq] += 1

# print search_lengths

print 'export search_lengths : ------------'
f = open('search_lengths.csv', 'w+')
for i in search_lengths:
  f.write(str(i) + ',' + str(search_lengths[i]) + '\n')
f.close()


data = ' '.join(data)
data = ' '.join(re.split(NONWORDS, data))
data = ' '.join([w for w in data.split() if w not in STOPWORDS])


text= data

tokens = nltk.word_tokenize(text)
tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
bi_tokens = list(bigrams(tokens))
tri_tokens = list(trigrams(tokens))

n_count = 500


fdist = nltk.FreqDist(tokens)
top_unigrams = list(map(list,fdist.most_common(n_count)))

# fdist.plot(100)

#print results
print 'export unigrams : ------------'
f = open('top_unigrams.csv', 'w+')
for i in range(len(top_unigrams)):
  f.write(str(top_unigrams[i][0]) + ',' + str(top_unigrams[i][1]) + '\n')
f.close()


fdist_bi = nltk.FreqDist(bi_tokens)
top_bigrams = list(map(list,fdist_bi.most_common(n_count)))

print 'export bigrams : ------------'
f = open('top_bigrams.csv', 'w+')
for i in range(len(top_bigrams)):
  f.write(string.replace(str(top_bigrams[i][0]),',','') + ',' + str(top_bigrams[i][1]) + '\n')
f.close()



fdist_tri = nltk.FreqDist(tri_tokens)
top_trigrams = list(map(list,fdist_tri.most_common(n_count)))

print 'export trigrams : ------------'
f = open('top_trigrams.csv', 'w+')
for i in range(len(top_trigrams)):
  f.write(string.replace(str(top_trigrams[i][0]),',','') + ',' + str(top_trigrams[i][1]) + '\n')
f.close()


tetra_tokens = list(ngrams(tokens, 4))
fdist_tetra = nltk.FreqDist(tetra_tokens)
top_tetragrams = list(map(list,fdist_tetra.most_common(n_count)))

print 'export tetragrams : ------------'
f = open('top_tetragrams.csv', 'w+')
for i in range(len(top_tetragrams)):
  f.write(string.replace(str(top_tetragrams[i][0]),',','') + ',' + str(top_tetragrams[i][1]) + '\n')
f.close()

# for grams in sixgrams:
#   print grams



# sorted_final_unigram = sorted(unigram_freq.items(), key=operator.itemgetter(1), reverse=True)

# print [(item, tri_tokens.count(item)) for item in sorted(set(tri_tokens))]




