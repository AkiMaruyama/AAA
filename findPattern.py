from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import urllib.request
import nltk 
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.chunk import RegexpParser
from re import findall,search 

URL = ['http://awardviewer.fwo.gov.au/award/show/MA000054#TopOfPage',
		'http://awardviewer.fwo.gov.au/award/show/MA000118#TOPOFBODYPAGE',
		'http://awardviewer.fwo.gov.au/award/show/MA000018#TopOfPage']


def extract_condition(url, patterns, example):
	
	# download webpage from url
	response = urllib.request.urlopen(url) 
	html = response.read() 
	soup = BeautifulSoup(html,"html5lib") 
	text = soup.get_text(strip=True) 
	sent_tokens = sent_tokenize(text)

	results = []
	punctuation = '!"#$&\'()*+,-/;<=>?@[\\]^_`{|}~'
	lemmatizer = WordNetLemmatizer()
	
	example_tokens = [lemmatizer.lemmatize(token) for token in word_tokenize(example)]
	clean_tokens = example_tokens[:]
	sr = stopwords.words('english')
	
	for token in example_tokens:
	    if token in stopwords.words('english'):
	        clean_tokens.remove(token)
	sentences = []
	for sent in sent_tokens:
		if all(pattern in sent or pattern.capitalize() in sent for pattern in patterns):
			tokens = word_tokenize(sent)
			tokens = [''.join(c for c in s if c not in punctuation) for s in tokens]
			tokens = [s for s in tokens if s]
			results.append(tokens)
			sentences.append(sent)

	scores = []
	for each in results:
		score = 0
		for i in clean_tokens:
			if i in each:
				score+=1
		scores.append(score)

	max_score = 0
	index = -1
	for idx,val in enumerate(scores):
		if val > max_score:
			max_score = val
			index = idx
	return (sentences[index])

#extract_condition(URL[2], ordinary_hours_patterns, ordinary_hours_example)

def extract_ordinary_hours(url):
	ordinary_hours_patterns = ["ordinary", "hour", "am", "pm"]
	ordinary_hours_example = "The ordinary hours of work will be between 6.00 am and 9.00 pm Monday to Sunday."
	result = extract_condition(url, ordinary_hours_patterns, ordinary_hours_example)
	hours = findall(r"(\d+\.\d+) [a|p]m",result)
	for i in range(len(hours)):
		hours[i] = str(int(float(hours[i])))
	return (hours)

def extract_max_daily_hours(url):
	max_daily_pt = ["ordinary", "hour"]
	max_daily_ep = "maximum length ordinary hours one shift exceed 10 hours meal breaks required day worked"
	result = extract_condition(url, max_daily_pt, max_daily_ep)
	# print (result)
	hours = findall(r"(\d+) [ordinary ]?hours",result)
	return (hours)

def extract_max_weekly_hours(url):
	pt = ["ordinary", "hour", "week"]
	ep = "The ordinary hours of work will be an average of 38 hours per week over a four week cycle"
	result = extract_condition(url, pt, ep)
	# print (result)
	hours = findall(r"(\d+) [hours ]?per week",result)
	return (hours)

def extract_public_rate(url):
	pt = ["rate", "paid", "public", "holiday"]
	ep = "ordinary hours performed on a public holiday must be paid at the rate of double time and a half for all hours of work."
	result = extract_condition(url, pt, ep)
	# print (result)
	hours = findall(r"of ([a-z]+) time",result)[0]
	return (hours)

def extract_casual_loading(url):
	pt = ["casual", "paid", "rate", "employee"]
	ep = "A casual employee must be paid per hour at the rate of 1/38th of the weekly rate prescribed for the class of work performed,plus 25%."
	result = extract_condition(url, pt, ep)
	# print (result)
	rate = findall(r"(\d+)%",result)[0]
	return (rate)

# def extract_sunday_rate(text):
# 	return pattern[0].title()


# extract_ordinary_hours(URL[1])
# extract_max_daily_hours(URL[1])
# extract_max_weekly_hours(URL[1])
# extract_public_rate(URL[1])
# extract_casual_loading(URL[1])

