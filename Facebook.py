"""
Kyle's part

"""
import facebook
import requests
import json
import nltk
import cPickle
import getopt
import sys
import json
from textblob import TextBlob


def get_post_sentiment(tweet):
    analysis = TextBlob(removeUnicode(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char
	return asciiText



access_token = ''
# Look at Bill Gates's profile for this example by using his Facebook id.
user = 'Google'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')
profile = graph.get_object("Google/feed")
#profile = graph.get_object("Google/statuses")

Jstr = json.dumps(profile)
JDict = json.loads(Jstr)
parsed_post = {}

pneg = 0
pnum = 0
pneu = 0
demwords = ""
wordies = []

for i in JDict['data']:
#Limited to 10
    print removeUnicode(i['message'])
    currentpost = removeUnicode(i['message'])
    parsed_post['text'] = currentpost
    
    parsed_post['sentiment'] = get_post_sentiment(currentpost)
    #adding to list of words
    demwords += parsed_post['text'].encode('utf-8').strip()
    
    wordies += [ w for w in currentpost.split() ]

    if parsed_post['sentiment'] == "positive":
        pnum += 1
    elif parsed_post['sentiment'] == "negative":
        pneg += 1
    elif parsed_post['sentiment'] ==  "neutral":
        pneu += 1

    print "Positive in ",pnum
    print "Negative in ",pneg
    print "Neutral in ",pneu
    lexical_diversity = 1.0 * len(set(wordies)) / len(wordies)
    print "Lexical Diversity of all posts:",lexical_diversity
    
    #Formatting
    print ""
    print "-----------"
    print ""
