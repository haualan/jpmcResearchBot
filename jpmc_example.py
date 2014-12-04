from __future__ import print_function
from alchemyapi import AlchemyAPI
import json


# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

f = open('/Users/ahau/src/test/alchemyapi_python/' + 'jpmc_abstract.txt')
demo_text = [line.rstrip('\n') for line in f]

demo_text = ' '.join(demo_text)
print(demo_text)
# print( len(demo_text),demo_text[0])


print('############################################')
print('#   Keyword Extraction Example             #')
print('############################################')
print('')
print('')

# print('Processing text: ', demo_text[0])
print('')

response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    print('there are this many keywords: ', len(response['keywords']))
    for keyword in response['keywords']:
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'])
        print('sentiment: ', keyword['sentiment']['type'])
        if 'score' in keyword['sentiment']:
            print('sentiment score: ' + keyword['sentiment']['score'])
        print('')
else:
    print('Error in keyword extaction call: ', response['statusInfo'])

print('############################################')
print('#   Concept Tagging Example                #')
print('############################################')
print('')
print('')

print('Processing text: ', demo_text)
print('')

response = alchemyapi.concepts('text', demo_text)

if response['status'] == 'OK':
    print('## Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Concepts ##')
    for concept in response['concepts']:
        print('text: ', concept['text'])
        print('relevance: ', concept['relevance'])
        print('')
else:
    print('Error in concept tagging call: ', response['statusInfo'])


print('')
