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
# download webpage from url
response = urllib.request.urlopen(URL[2]) 
html = response.read() 
soup = BeautifulSoup(html,"html5lib") 
text = soup.get_text(strip=True) 

sent_tokens = sent_tokenize(text)
patterns = ["ordinary", "hour", "am", "pm"]

results = []
punctuation = '!"#$%&\'()*+,-/;<=>?@[\\]^_`{|}~'

lemmatizer = WordNetLemmatizer()
example = "The ordinary hours of work will be between 6.00 am and 9.00 pm Monday to Sunday."
example_tokens = [lemmatizer.lemmatize(token) for token in word_tokenize(example)]
clean_tokens = example_tokens[:]
sr = stopwords.words('english')
for token in example_tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)
# print (clean_tokens)
sentences = []
for sent in sent_tokens:
	if all(pattern in sent or pattern.capitalize() in sent for pattern in patterns):
		tokens = word_tokenize(sent)
		# clean_tokens = tokens[:]
		# sr = stopwords.words('english')
		# for token in tokens:
		#     if token in stopwords.words('english'):
		#         clean_tokens.remove(token)
		# remove punctuation for result test
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

# print (scores)
print ("index is " + str(index))
print (sentences[index])



hours = findall(r"(\d+\.\d+) [a|p]m",sentences[index])
print (hours)
# synonyms = []
# for syn in wordnet.synsets(pattern):
#     for lemma in syn.lemmas():
#         synonyms.append(lemma.name())
# print(synonyms)


# stemmer = PorterStemmer() 
# print(stemmer.stem(pattern))

# lemmatizer = WordNetLemmatizer()
# print(lemmatizer.lemmatize('working', pos="v"))

# lemmatizer = WordNetLemmatizer()
# print(lemmatizer.lemmatize('hours'))

