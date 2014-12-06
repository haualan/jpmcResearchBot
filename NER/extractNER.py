import nltk, re
from nltk.chunk import RegexpParser
import os, sys
# need to add path so we can access parent folder for DB settings
sys.path.append('../')
import sample
import multiprocessing as mp
# import DB



def excludeKeywords(exclusion_list, iKeywords):
  # result = []
  exclusion_list = list(map(str.lower, exclusion_list))
  result = [i for i in iKeywords if i.lower() not in exclusion_list]

  return result

def constructTrainData(inclusion_list):
  result = []
  # result must be in the form of (list(list(tuple(str, str))))
  for i in inclusion_list:
    i_split = i.split()
    # capitalize first words, nltk tagger is case sensitive, we will attempt to tag exact exact strings and with forst word capitalized
    c = list(map(lambda s: s[0].upper()+s[1:], i_split))
    if len(i_split) == 1:
      result.append([(i_split[0],'JPNE1'),(c[0],'JPNE1')])
    elif len(i_split) == 2:
      result.append([ (i_split[0],'JPNE2'),(i_split[1],'JPNE2'), 
                      (c[0],'JPNE2'),(c[1],'JPNE2')
                    ])
    elif len(i_split) == 3:
      result.append([ (i_split[0],'JPNE3'),(i_split[1],'JPNE3'), (i_split[2],'JPNE3'),
                      (c[0],'JPNE3'),(c[1],'JPNE3'), (c[2],'JPNE3')
                    ])

  return result

def NE_fork(sentences):

  sentence = sentences[0]
  inclusion_list = sentences[1]

  # set trained tags
  traindata =  constructTrainData(inclusion_list)

  # define nltk taggers
  t0 = nltk.data.load(nltk.tag._POS_TAGGER)
  t1 = nltk.UnigramTagger(traindata, backoff=t0)
  t2 = nltk.BigramTagger(traindata, backoff=t1)

    # word_tokenize returns an array with each word as an item
  tokens = nltk.word_tokenize(sentence)

  # t2.tag tags words with part of speach
  pos_tags = t2.tag(tokens)

  #apply nltk chuncking to fine Named Entities
  chunked = nltk.ne_chunk(pos_tags, binary=True)

  # append results with standard NE
  NE = []
  for i in chunked:
    # print i

    if type(i) == nltk.tree.Tree: 
      # print 'i.leaves:'
      i_leaves = i.leaves()
      # print i_leaves
      term = []
      for j in i_leaves:
        term.append(j[0])
      term = ' '.join(term)
      NE.append(term)

  # Define your custom grammar (modified to be a valid regex).
  grammar = """ CHUNK: {<JPNE1>|<JPNE2><JPNE2>|<JPNE3><JPNE3><JPNE3>} """

  # Create an instance of your custom parser.
  custom_tag_parser = RegexpParser(grammar)

  # print custom_tag_parser.parse(pos_tags)

  # Parse!
  for i in custom_tag_parser.parse(pos_tags):
    if type(i) == nltk.tree.Tree: 
      # print 'i.leaves:'
      i_leaves = i.leaves()
      # print i_leaves
      term = []
      for j in i_leaves:
        term.append(j[0])
      term = ' '.join(term)
      NE.append(term)

  return NE

def findNamedEntities(raw_text, inclusion_list):

  # clear data from unicode text:
  # raw_text = unicode(raw_text, errors='ignore')

  # raw_text = removeNonAscii(raw_text)

  # # set trained tags
  # traindata =  constructTrainData(inclusion_list)

  # # define nltk taggers
  # t0 = nltk.data.load(nltk.tag._POS_TAGGER)
  # t1 = nltk.UnigramTagger(traindata, backoff=t0)
  # t2 = nltk.BigramTagger(traindata, backoff=t1)

  # # sentence is just your raw text input
  # sentence = raw_text

  # consider forking processes here and process each sentence to a thread
  pool = mp.Pool()
  sentence = nltk.sent_tokenize(raw_text)
  sentences = list(map(lambda x: [x, inclusion_list],sentence))

  # print sentences
  NE  = list(pool.map(NE_fork, sentences))


  NE = [num for elem in NE for num in elem]
  return NE


if __name__ == '__main__':

  inclusion_list = ['alan', 'Curie', 'today alan alan', 'business diversification']
  exclusion_list = ['Nasdaq']

  # con = DB.get_con()
  # inclusion_list = DB.getInclusionList()
  # exclusion_list = DB.getExclusionList()

  # print inclusion_list
 

  NE = findNamedEntities(sample.sample_text, inclusion_list)

  # print NE

  print 'EXAMPLE: Named Entities....................'
  # omit repeats and return lowercase
  NE = sorted(list(set(i.lower() for i in NE)))

  print 'EXAMPLE: filter NE....................'
  NE = excludeKeywords(exclusion_list, NE)

  print NE







 
  # for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
  #   print doc.text

  # IN = re.compile(r'.*\bin\b(?!\b.+ing)')
  # for rel in nltk.sem.extract_rels('ORG', 'LOC', sentence, corpus='ieer', pattern = IN):
  #   print(nltk.sem.rtuple(rel))


  # NAMED ENTITY RECOGNITION:
  # 1. break words into tokens 'my name is Alan' -> ['my','name','is','Alan']
  # 2. POS tagging, (my, is) holds no meaning... 'name' is a noun, 'Alan' is a Named ENTITY
  # 3. Add custom tags (training corpus)
  # 3b. find union of set
  # 4. return NER set

      