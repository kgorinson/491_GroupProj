# File: 	Twitter.py
# Author: 	Joanna Dinh
# Date: 	5/8/2017
#
# Description:
# 	This file connects to twitter and grabs tweets from @google, displaying each retweet count, likes, lexical diversity and sentiment analysis for every tweet
# 	User must input all credentials or manually hard code them into the program
# 	Expand window as big as possible to see all data

import twitter 
import json
from collections import Counter
from prettytable import PrettyTable
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

def getTwitterData():
	CONSUMER_KEY = raw_input("Enter CONSUMER_KEY: ")
	CONSUMER_SECRET = raw_input("Enter CONSUMER_SECRET: ")
	OAUTH_TOKEN = raw_input("Enter OAUTH_TOKEN: ")
	AUTH_TOKEN_SECRET = raw_input("Enter OAUTH_TOKEN_SECRET: ")

	print "\nConnecting to Twitter...\n"
	
	# CONNECT TO TWITTER
	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	tw = twitter.Twitter(auth=auth)
	
	# GOOGLE MESSAGES & LIKES/RETWEETS & LEXICAL DIVERSITY & SENTIMENT ANALYSIS
	print "Grabbing 25 @google...\n"
	getTweets('@google', 25, tw)
	
def getTweets(target, count, tw):
	tweets = tw.search.tweets(q=target, count=count, lang='en')
	texts = []
	likes = []
	retweets = []

	# Get tweets, likes, and retweet count
	for status in tweets["statuses"]:
		texts.append(status["text"])
		likes.append(status["favorite_count"])
		retweets.append(status["retweet_count"])
	
	# Create pretty table
	user_stats = PrettyTable(field_names=['#', 'Tweets', 'Likes', 'Retweets', 'Lexical Diversity', 'Sentiment Analysis'])

	# Grab data analysis
	for i in range(len(texts)):
		# Get tweet 
		message = removeUnicode(texts[i])
		
		# Create bag of words from text
		words = []
		for w in removeUnicode(texts[i]).split():
			words.append(w)		

		# Get likes, retweets, lexical diversity, sentiment analysis
		user_stats.add_row([i + 1, message, likes[i], retweets[i], getLexicalDiversity(words), getSentimentAnalysis(tweets["statuses"][i])])
	
	# Print pretty table
	user_stats.align = 'l'
	print user_stats
	print "*****************************************************************\n"

def removeUnicode(text):
	asciiText = ""
	
	for char in text:
		if (ord(char) < 128):
			asciiText = asciiText + char
			
	return asciiText
	
def getFreqCount(words, pt):
	cnt = Counter(words)
	srtCnt = sorted(cnt.items(), key=lambda pair: pair[1], reverse=True)
	for kv in srtCnt:
		pt.add_row(kv)

def getSentimentAnalysis(gmrText):	
	if (gmrText["user"]["description"] is not None) and (gmrText["user"]["location"] is not None):
		vs = vaderSentiment(gmrText["text"].encode('utf-8'))
		sentimentAnalysis = vs['compound']
		return sentimentAnalysis
					
def getLexicalDiversity(words):
	lexicalDiversity = 1.0*len(set(words))/len(words)
	return lexicalDiversity

getTwitterData()