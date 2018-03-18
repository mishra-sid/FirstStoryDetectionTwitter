import math
import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from time import time
from textblob import TextBlob as tb


class TFIDF(object):

    def __init__(self, texts, langue):

        nltk.download("rslp")

        self.texts = texts
        self.langue = langue
        self._row_axis, self._col_axis = 0, 1

        self._df = pd.DataFrame(
            data={'TEXT': self.texts, 'ID': range(len(self.texts))})
        
    def _to_lower_case(self, text):
    
        text = text.lower()

        return text

    def _remove_stopwords(self, text):
        nltk.download('stopwords')
        pt_stop = stopwords.words('english')
        self._tokenizer = RegexpTokenizer(r'\w+')
        
        tokens = self._tokenizer.tokenize(text)
        stopped_tokens = list(filter(lambda t: t not in pt_stop, tokens))
        without_stopwords = " ".join(stopped_tokens)
        return without_stopwords

    def _tf(self, word, blob):
        return blob.words.count(word) * 1.0 / len(blob.words)

    def _n_containing(self, word, bloblist):
        return len(list(filter(lambda blob: word in blob, bloblist)))

    def _idf(self, word, bloblist):
        n_textos = len(bloblist)
#         print (1 + self._n_containing(word, bloblist))
        return math.log(n_textos + 0.0000000001 / (1 + self._n_containing(word, bloblist)))

    def _tfidf(self, word, blob, bloblist):
        
        tempvalue = self._tf(word, blob) * 1.0* self._idf(word, bloblist)
#         print self._idf(word, bloblist)
        return tempvalue
    
    def _get_text_radicals(self, text):

        stemmer = nltk.RSLPStemmer()
        blob = tb(text)
        radicals = [stemmer.stem(word) for word in blob.words]
        text_radicals = " ".join(radicals)

        return text_radicals

    def _get_important_radicals(self, text):
        blob = tb(text)
        scores = {radical: self._tfidf(radical, blob, self.columns_radicals)
                  for radical in blob.words}
        median_score = np.median(list(scores.values()))
        
        important_radicals = list(
            filter(lambda x: x[1] >= median_score, scores.items()))
        return important_radicals

    def _extract_tokens(self):
#         print type(self._df)
        # lower case the text
        self._df['TEXT'] = self._df.apply(
            lambda row: self._to_lower_case(row['TEXT']), axis=self._col_axis)
        
        # text without stopwords
        without_stopwords = self._df['TEXT'].apply(
            lambda x: self._remove_stopwords(x)
        )
        
        # create seperate column, we will remove them later
        self._df['WITHOUT_STOPWORDS'] = without_stopwords
        
        
        # compute root words of the text , like extracted becomes ectract , works like died, dies, die, they become die

        self._df['TEXT_OF_RADICALS'] = self._df['WITHOUT_STOPWORDS'].apply(
            lambda x: self._get_text_radicals(x)
        )

        # create a column for the radicals
        self.columns_radicals = list(self._df['TEXT_OF_RADICALS'])
        
        # extract important radicals based on tf idf scores important_radicals
        
        important_radicals = self._df['TEXT_OF_RADICALS'].apply(
            lambda text: self._get_important_radicals(text)
        )
        
#         print important_radicals
        # filter important radicals 
        self._df['IMPORTANT_RADICALS'] = important_radicals.apply(
            lambda radicals_scores: [r for r, s in radicals_scores]
        )
        
        # put in pandas dataframe with just the last column
        
        aux = self._df
        self._df = pd.DataFrame(data={})
        self._df['IMPORTANT_RADICALS'] = aux['IMPORTANT_RADICALS']
        
       
        
    def _conc_my_tokens(self, tokens, i):
        if type(tokens) == list:
            self.tokens_texts[i] += tokens
        
    def get_sparse_matrix(self):

        self._extract_tokens()
        words_set = []
        
        # put all the detected important radicals in a list
        for l in list(self._df['IMPORTANT_RADICALS']):
            words_set += l
        
        # set the list , math meaning of set not english
        words_set = list(set(words_set))
        
        # create dictionary out of the important radicals for each document, stored in self.token_texts
        self.tokens_texts = {i: [] for i in range(len(self.texts))}
        
        for i in range(len(self.texts)):
            self._df.apply(lambda row: self._conc_my_tokens(
                row[i], i), axis=self._row_axis)
        
        # Finally create a sparse matrix, for each document
        matrix = [[None] * len(words_set) for i in range(len(self.texts))]
        for text in range(len(self.texts)):
            for i, token in enumerate(words_set):
                has = 1 if token in self.tokens_texts[text] else 0
                matrix[text][i] = has

        return matrix


# In[ ]:


## use as

##textos = ["nice  similarly buoy","This is a buoy important sentence", "This is also similarly an important sentence"]

## tfidf = TFIDF(textos, 'english')
## sparse_matrix = tfidf.get_sparse_matrix()


