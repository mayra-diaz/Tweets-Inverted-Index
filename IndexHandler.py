from InvertedIndex import InvertedIndex
from Util import Util
import numpy as np

class IndexHandler():

    def __init__(self):
        self.util = Util()
        self.inverted_index = InvertedIndex()

    def add(self, d):
        self.inverted_index.add(d)

    def analyze_query(self, text, n):
        tokens = self.util.pre_process(text)
        query_tf = {}
        for token in tokens:
            if token in query_tf:
                query_tf[token] += 1
            else:
                query_tf[token] = 1
        query_tf_idf = {}
        for token, tf in query_tf.items():
            query_tf_idf[token] = self.util.weight_td_idf(tf, self.inverted_index.get_token_df(token), self.inverted_index.get_number_of_tweets())
        index_docs_weights = self.inverted_index.get_index_interseccion_with_query(query_tf.keys())
        query = np.array(list(query_tf_idf.values()))
        result = {}
        for id, weights in index_docs_weights.items():
            result[id] = self.cosine_distance(query, np.array(list(weights)))
        final = dict(sorted(result.items(), key=lambda x: x[0], reverse=True))
        return self.inverted_index.get_tweets(list(final.keys()))[:n]
        
    def cosine_distance(self, q, doc):
        q = np.log10(1 + q) 
        doc = np.log10(1 + doc) 
        return np.dot(q, doc) / (np.linalg.norm(q) * np.linalg.norm(doc))
