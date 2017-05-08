"""
491 Group Project
Spring 2017

"""
import facebook
import requests
import json
import nltk
import cPickle
import getopt
import sys
import json
import twitter 
import json
from collections import Counter
from prettytable import PrettyTable
	
from bs4 import BeautifulSoup
import requests
import nltk
import russell as ru
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

from textblob import TextBlob

def scrapePage():
	page = "https://www.google.com/intl/en/policies/technologies/"
	print "------------------------"
	print "     Page: ", page
	print "------------------------"

	html = requests.get(page)
	soup = BeautifulSoup(html.text, 'html5lib')
	all_paras = soup.find_all('p')
	data_2017 = ""
	for para in all_paras:
		data_2017 = data_2017 + para.text
		article_sum = ru.summarize(data_2017)

	print "------------------------"
	print "  Three Sentence Summary"
	print "------------------------"
	for sent in article_sum['top_n_summary']:
		print removeUnicode(sent)

	asc_2017 = removeUnicode(data_2017)
	lstSent = nltk.tokenize.sent_tokenize(asc_2017)
	sentWords = [nltk.tokenize.word_tokenize(s) for s in lstSent]
	posWords = [nltk.pos_tag(w) for w in sentWords]
	posWords = [token for sent in posWords for token in sent]

	chunkCollector = []
	foundChunk = []
	lastPos = None
	for (token, pos) in posWords:
		if pos == lastPos and pos.startswith('NN'):
			foundChunk.append(token)
		elif pos.startswith('NN'):
			if foundChunk != []:
				#something in hopper so add to collection
				chunkCollector.append((''.join(foundChunk), pos))
			foundChunk = [token]
		lastPos = pos

	dChunk = {}
	for chunk in chunkCollector:
		dChunk[chunk] = dChunk.get(chunk,0) + 1


	print "------------------------"
	print " Most Common Noun Usage"
	print "------------------------"
	for (entity, pos) in sorted(dChunk, key=dChunk.get, reverse=True)[:7]:
		print '\t%s (%s)' % (entity, dChunk[entity,pos])

	chunkCollector = []
	foundChunk = []
	lastPos = None
	for (token, pos) in posWords:
		if pos == lastPos and pos.startswith('V'):
			foundChunk.append(token)
		elif pos.startswith('V'):
			if foundChunk != []:
				#something in hopper so add to collection
				chunkCollector.append((''.join(foundChunk), pos))
			foundChunk = [token]
		lastPos = pos

	dChunk = {}
	for chunk in chunkCollector:
		dChunk[chunk] = dChunk.get(chunk,0) + 1

	print "------------------------"
	print " Most Common Verb Usage"
	print "------------------------"
	for (entity, pos) in sorted(dChunk, key=dChunk.get, reverse=True)[:7]:
		print '\t%s (%s)' % (entity, dChunk[entity,pos])

def getFreqCount(words, pt):
	cnt = Counter(words)
	srtCnt = sorted(cnt.items(), key=lambda pair: pair[1], reverse=True)
	for kv in srtCnt:
		pt.add_row(kv)




def getTwitterData():
	CONSUMER_KEY = raw_input("Enter CONSUMER_KEY: ")
	CONSUMER_SECRET = raw_input("Enter CONSUMER_SECRET: ")
	OAUTH_TOKEN = raw_input("Enter OAUTH_TOKEN: ")
	OAUTH_TOKEN_SECRET = raw_input("Enter OAUTH_TOKEN_SECRET: ")
	
	# CONNECT TO TWITTER
	print "\nConnecting to Twitter...\n"
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	tw = twitter.Twitter(auth=auth)
	
	# GOOGLE MESSAGES & LIKES/RETWEETS & LEXICAL DIVERSITY & SENTIMENT ANALYSIS
	getTweets('@google', 50, tw)
	
def getTweets(target, count, tw):
	tweets = tw.search.tweets(q=target, count=count, lang='en')
	texts = []
	likes = []
	retweets = []
	location = []
	
	# Get tweets, likes, location, and retweet count
	for status in tweets["statuses"]:
		texts.append(status["text"])
		likes.append(status["favorite_count"])
		retweets.append(status["retweet_count"])
		
		if status["user"]["location"]:
			location.append(status["user"]["location"])
		else:
			location.append("N/A")
		
	# Create pretty table
	user_stats = PrettyTable(field_names=['#', 'Tweets', 'Likes', 'RT','GEOLOC', 'LD', 'SA'])
	user_stats_two = PrettyTable(field_names=['#', 'Tweets', 'Likes', 'RT','GEOLOC', 'LD', 'SA'])
	# Grab data analysis
	for i in range(len(texts)):
		# Get tweet 
		message = removeUnicode(texts[i])
		
		# Create bag of words from text
		words = []
		length = len(texts) 
		for w in removeUnicode(texts[i]).split():
			words.append(w)		

		# Get likes, retweets, location, lexical diversity, sentiment analysis
		# first set of tweets 
		if i < length/2:
			user_stats.add_row([i + 1, message, likes[i], retweets[i], location[i], getLexicalDiversity(words), getSentimentAnalysis(tweets["statuses"][i])])
		# second set of tweets 
		else:
			user_stats_two.add_row([i + 1 - length/2, message, likes[i], retweets[i], location[i], getLexicalDiversity(words), getSentimentAnalysis(tweets["statuses"][i])])

	user_stats.align = 'l'
	user_stats_two.align = 'l'

	# Print pretty table	
	print "Grabbing a set of " + str(length/2) + " tweets @google..."
	print user_stats
	print "\nGrabbing another set of " + str(length/2) + " tweets @google..."
	print user_stats_two


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


	

def getSentimentAnalysis(gmrText):	
	if (gmrText["user"]["description"] is not None) and (gmrText["user"]["location"] is not None):
		vs = vaderSentiment(gmrText["text"].encode('utf-8'))
		sentimentAnalysis = vs['compound']
		return sentimentAnalysis
					
def getLexicalDiversity(words):
	lexicalDiversity = 1.0*len(set(words))/len(words)
	return lexicalDiversity







scrapePage()
