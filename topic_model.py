
from gensim import corpora, models
import gensim

class topic_model:
    def __init__(self, stories):
        self.stories = stories
        self.texts = [ ]
        for story in stories:
            self.texts.append(story['story'])

    def trainModel(self):
        self.dictionary = corpora.Dictionary(texts)
        
        self.corpus = [self.dictionary.doc2bow(text) for text in texts]
        self.ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)
        
