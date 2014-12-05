import NER.extractNER as NER
import TFIDF.extractTFIDF as TFIDF
import DB
import sample

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

inclusion_list = DB.getInclusionList()
exclusion_list = DB.getExclusionList()

n = 10

istr = sample.sample_text
istr = removeNonAscii(istr)

NER_results = NER.findNamedEntities(istr, inclusion_list)

TFIDF_results = TFIDF.findTFIDFkeywords(istr)

keywords = NER_results[0:n/2] + TFIDF_results[0:n/2]

# omit repeats and return lowercase
keywords = sorted(list(set(i.lower() for i in keywords)))
keywords = NER.excludeKeywords(exclusion_list, keywords)

print keywords