## Group Project for 491 UMBC


## Assignment
# Due May 8th
Pick a high tech company you are interested in investigating. Analyze the company’s social
media: Twitter, Facebook public pages, web site, the official blog or independent blogs
related to company. Explain what language and tools you used and why. Consider using
each of the following access or mining techniques as you deem appropriate - explain why
you selected what you did:


### Reference:

[Project 1](https://github.com/kgor93/491_GroupProj/blob/master/proj1.py)

### Setup commands
- sagi prettytable
- pip install prettytable
- pip install twitter json nltk cPickle getopt sys textblob
- pip install tweepy==3.3.0
- pip install --upgrade pip
- pip install requests
- pip install pyquery
- pip install fake_useragent
- pip install faker
- pip install requests
- pip install pyquery
- pip install tweepy==3.3.0
- python -m pip install twitter facebook-sdk
- pip install basc-py4chan
- python -m pip install twitter facebook-sdk vaderSentiment==0.5 html5lib BeautifulSoup bumpy nltk
- python 491_proj1.py 
- pip install TextBlob

---------------------------------

- *Search for tweets
- *Tweet trending
- *Next search results
- *Tweet users and entities
- *Lexical Diversity
- *Retweets
- *Likes and Frequency analysis
- *Screen Scraping
- *Facebook public page commentary
- *Sentiment analysis
- *TDM
- *EOS and Freq Dist
- *POS, Chunking, Extraction
- *Summarization techniques
- *N-Grams
- *TF-IDF
- *Cosine Similarity
- *Associations
- *Geocoding



```
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




CONSUMER_KEY = "Q55QaphWqwHyVW4AblGHfZ1Gv"
CONSUMER_SECRET = "KjXBieS2wNbx22yo0vepgWfRsZVfImq8zzxLoifJIMA86Pqhm3"
OAUTH_TOKEN = "1915750028-Dv4A8wXfJeCoRqKKMVPD6FwHpjTjXudO4nI5YXM"
OAUTH_TOKEN_SECRET = "zQKflAtjkjYdOymo04csDAquHw5lpl3XpvD3ePPv5qoR0"

auth2 = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)


tw = twitter.Twitter(auth=auth2)

coke = tw.statuses.user_timeline(screen_name = "cocacola",count=25)#getuser("cocacola",25)
pepsi = tw.statuses.user_timeline(screen_name = "pepsi",count=25)

forloop(coke,"coke")
forloop(pepsi,"pepsi")




```




We've done a lot of this already in project 1. The bolded parts are the parts we haven't done.

- *Search for tweets
- *Tweet trending
- *Next search results
- *Tweet users and entities
- *Lexical Diversity
- *Retweets
- *Likes and Frequency analysis
**- Screen Scraping**
**- Facebook public page commentary**
- *Sentiment analysis
**- TDM
- EOS and Freq Dist
- POS, Chunking, Extraction
- Summarization techniques**
**- N-Grams
- TF-IDF
- Cosine Similarity
- Associations
- Geocoding**

All of these have easy to use API packages. This shouldn't be too difficult at all.
