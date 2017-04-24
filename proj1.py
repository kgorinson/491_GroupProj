import twitter
import json
import nltk
import cPickle
import getopt
import sys
import json
from collections import Counter
from prettytable import PrettyTable
from textblob import TextBlob


def getuser(name,num):
    return api.user_timeline(screen_name = name,count=num)

def removeUnicode(text):
	asciiText=""
	for char in text:
		if(ord(char)<128):
			asciiText=asciiText + char
	return asciiText

def get_tweet_sentiment(tweet):
    analysis = TextBlob(removeUnicode(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def forloop(item,name):
    sodawords = ""
    pnum = 0
    pneg = 0
    pneu = 0
    words = []
    for status in item:
        print ""
        currenttweet = removeUnicode(status["text"])
        print currenttweet
        parsed_tweet = {}
        # saving text of tweet
        parsed_tweet['text'] = currenttweet
        parsed_tweet['sentiment'] = get_tweet_sentiment(currenttweet)
        print "Favorite count:",status["favorite_count"]
        print "Retweet count:",status["retweet_count"]
        print "The sentiment is:",parsed_tweet['sentiment']
        print ""
        #sodawords += str(tweet.text)
        sodawords += parsed_tweet['text'].encode('utf-8').strip()
        words += [ w for w in currenttweet.split() ]
        if parsed_tweet['sentiment'] == "positive":
            pnum += 1
        elif parsed_tweet['sentiment'] == "negative":
            pneg += 1
        elif parsed_tweet['sentiment'] ==  "neutral":
            pneu += 1
    print "Positive in",name,pnum
    print "Negative in",name,pneg
    print "Neutral in",name,pneu
    lexical_diversity = 1.0 * len(set(words)) / len(words)
    print "Lexical Diversity of all tweets:",lexical_diversity
    print "----------------------"




CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

auth2 = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)


tw = twitter.Twitter(auth=auth2)

coke = tw.statuses.user_timeline(screen_name = "cocacola",count=25)#getuser("cocacola",25)
pepsi = tw.statuses.user_timeline(screen_name = "pepsi",count=25)

forloop(coke,"coke")
forloop(pepsi,"pepsi")

