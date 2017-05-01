from bs4 import BeautifulSoup
import requests
import nltk
import russell as ru


def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char
	return asciiText


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


scrapePage()

