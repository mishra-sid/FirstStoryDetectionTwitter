import math
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import numpy as np
from constants import *

class TFIDF_optim:

    def __init__(self, stories):
        self.stories = stories
        self.ref = {}
        self.len_docs = len(self.stories)
        self._tokenizer = RegexpTokenizer(r'\w+')
    
    def sanitize(self):
        stops = stopwords.words('english')
        stemmer = nltk.stem.SnowballStemmer('english')

        for ind in range(self.len_docs):
            self.stories[ind]['story'] = self.stories[ind]['story'].lower()
            tokens = self._tokenizer.tokenize(self.stories[ind]['story'])
            stopped_tokens = list(filter(lambda t : t not in stops, tokens))
            radicals = [ stemmer.stem(word) for word in stopped_tokens ]
            self.stories[ind]['story'] = radicals
            for word in radicals:
                self.ref[word] = { 'count' : 0, 'denominator' : 0, 'occured': 0, 'score': 0.0 }

    def tfidf(self):
        self.sanitize()
        for story in self.stories:
            for word in story['story']:
                self.ref[word]['count'] += 1
                if self.ref[word]['occured'] == 0:
                    self.ref[word]['denominator'] += 1
                    self.ref[word]['occured'] = 1
            for word in story['story']:
                self.ref[word]['occured'] = 0 
        
        self.len_words = len(self.ref.keys())
        
        print(self.len_words , self.len_docs)
        
        for word in self.ref:
            tf = self.ref[word]['count']/float(self.len_words)
            idf = math.log( float(self.len_docs) / self.ref[word]['denominator'] + 0.000000001)
            self.ref[word]['score'] = tf * idf
    
    def get_important_words(self):
        median_score = np.median( [ self.ref[word]['score'] for word in self.ref ] )

        important_words = [ [ k, self.ref[k]['count']] for k in self.ref if self.ref[k]['score'] >= median_score * FRACTION_IMPORTANT_WORDS_THRESHOLD ]

        return important_words


        

