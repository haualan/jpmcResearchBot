#!flask/bin/python
from flask import Flask, jsonify, request, abort
import NER
import DB

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]



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

@app.route('/', methods=['POST'])
def create_task():
    if not request.get_json(force=True) or not 'text' in request.get_json(force=True):
        print 'aborting'
        abort(400)
    # istr = request.json['text']
    istr = request.get_json(force=True)['text'] 

    inclusion_list = DB.getInclusionList()
    exclusion_list = DB.getExclusionList()

    keywords = NER.findNamedEntities(istr, inclusion_list)

    # keywords = ['foo','bar', istr]

    # omit repeats and return lowercase
    keywords = sorted(list(set(i.lower() for i in keywords)))

    # exclude certain keywords
    keywords = NER.excludeKeywords(exclusion_list, keywords)



    return jsonify({'keywords': keywords}), 201


if __name__ == '__main__':
    app.run(debug=True)