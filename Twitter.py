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
	
