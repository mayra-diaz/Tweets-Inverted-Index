import os
import glob
from math import log10

import nltk
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')

class Util():

    def __init__(self) -> None:
        self.stopWordsFile = './stopWords/stop-words-spanish.txt'

    def clear_dir(self, directory):
        filelist = glob.glob(os.path.join(directory, "*"))
        for f in filelist:
            os.remove(f)

    def pre_process(self, text):
        tokens = []
        if isinstance(text, str):
            tokens = nltk.word_tokenize(text.lower())
        else:
            # Tokenizar el texto
            for line in text:
                tokens += nltk.word_tokenize(line.lower())

        # Retirar signos innecesarios
        with open('symbols.txt') as file:
            symbol_list = [line.lower().strip() for line in file]
        for word in tokens:
            if word in symbol_list:
                tokens.remove(word)
            
        #Filtrar stoptokens
        clean_tokens = []
        with open(self.stopWordsFile) as file:
            stoplist = [line.lower().strip() for line in file]
        for token in tokens:
            if not token in stoplist:
                clean_tokens.append(token)
            
        # Reducir palabras a su raiz
        stemmer = SnowballStemmer('spanish')
        root_tokens = []
        for word in clean_tokens:
            root_tokens.append(stemmer.stem(word))
        return root_tokens

    def weight_td_idf(self, tfd, dtf, n):
        try:
            return log10(1 + tfd) * log10(n/dtf)
        except:
            return 0
