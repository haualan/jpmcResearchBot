#!flask/bin/python
from flask import Flask, jsonify, request, abort
import NER.extractNER as NER
import TFIDF.extractTFIDF as TFIDF
import DB

app = Flask(__name__)

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

# @app.route('/<string:istr>', methods=['GET'])
# def get_tasks(istr):
#     keywords = ['foo','bar','roo']
#     keywords.append(istr)
#     # print 'istr',istr
#     # print keywords.append(istr)
#     return jsonify({'keywords': keywords})



# @app.route('/', methods=['POST'])
# def create_task():
#     if not request.form or not 'text' in request.form:
#         # print 'aborting'
#         abort(400)
#     istr = request.form['text']
#     keywords = ['foo','bar', istr]
#     return jsonify({'keywords': keywords}), 201


# @app.route('/', methods=['POST'])
# def test():

#     return jsonify({'keywords': "hello"}), 201

@app.route('/getKeywords', methods=['POST'])
def getKeywords():
    if not request.get_json(force=True) or not 'text' in request.get_json(force=True):
        print 'aborting'
        abort(400)


    # istr = request.json['text']
    istr = request.get_json(force=True)['text'] 
    n = int(request.get_json(force=True)['max_n'] )
    # remove all nonAsciiCharacters
    istr = removeNonAscii(istr)

    inclusion_list = DB.getInclusionList()
    exclusion_list = DB.getExclusionList()

    istr = removeNonAscii(istr)

    NER_results = NER.findNamedEntities(istr, inclusion_list)
    NER_results = list(set(NER_results))

    TFIDF_results = TFIDF.findTFIDFkeywords(istr)

    keywords = NER_results[0:n/2] + TFIDF_results[0:n/2]

    # omit repeats and return lowercase
    keywords = sorted(list(set(i.lower() for i in keywords)))

    current_j = n/2
    current_k = n/2
    while len(keywords) < n:
        if current_k < len(NER_results):
            current_k += 1
            if NER_results[current_k] not in keywords:
                keywords.append(NER_results[current_k])
        else:
            current_j += 1
            if TFIDF_results[current_j] not in keywords:
                keywords.append(TFIDF_results[current_j])
    
    keywords = NER.excludeKeywords(exclusion_list, keywords)



    return jsonify({'keywords': keywords}), 201

@app.route('/getNER', methods=['POST'])
def getNER():
    if not request.get_json(force=True) or not 'text' in request.get_json(force=True):
        print 'aborting'
        abort(400)


    # istr = request.json['text']
    istr = request.get_json(force=True)['text'] 
    n = int(request.get_json(force=True)['max_n'] )
    # remove all nonAsciiCharacters
    istr = removeNonAscii(istr)

    inclusion_list = DB.getInclusionList()
    exclusion_list = DB.getExclusionList()

    istr = removeNonAscii(istr)

    NER_results = NER.findNamedEntities(istr, inclusion_list)

    keywords = NER_results[0:n]

    # omit repeats and return lowercase
    keywords = sorted(list(set(i.lower() for i in keywords)))
    keywords = NER.excludeKeywords(exclusion_list, keywords)



    return jsonify({'keywords': keywords}), 201

@app.route('/getTFIDF', methods=['POST'])
def getTFIDF():
    if not request.get_json(force=True) or not 'text' in request.get_json(force=True):
        print 'aborting'
        abort(400)


    # istr = request.json['text']
    istr = request.get_json(force=True)['text'] 
    n = int(request.get_json(force=True)['max_n'] )
    # remove all nonAsciiCharacters
    istr = removeNonAscii(istr)

    inclusion_list = DB.getInclusionList()
    exclusion_list = DB.getExclusionList()

    istr = removeNonAscii(istr)

    TFIDF_results = TFIDF.findTFIDFkeywords(istr)

    keywords = TFIDF_results[0:n]


    keywords = NER.excludeKeywords(exclusion_list, keywords)



    return jsonify({'keywords': keywords}), 201

if __name__ == '__main__':
    app.run(debug=True)