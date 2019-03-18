
'''
Authors: Manas Gaur, Amanuel Alambo
Instructor: Dr. keke Chen
   utility functions for processing terms

    shared by both indexing and query processing
'''
import cran
import nltk
from nltk.tokenize import word_tokenize

from nltk.stem.snowball import SnowballStemmer


def isStopWord(word):
    ''' using the NLTK functions, return true/false'''

    # ToDo
    #returns true of a word passed is a stop word
    with open('stopwords', 'r') as f:
	   stop_words = f.read()
    return word in stop_words
    #####

def stemming(word):
    ''' return the stem, using a NLTK stemmer. check the project description for installing and using it'''

    # ToDo
    ##SnowballStemmer
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    return stemmer.stem(word)
    #######

#splitting a doc
def splitDoc(doc):
    tokens = word_tokenize(doc)
    words = [word for word in tokens if word.isalpha()]   #punctuation removal
    words = [word for word in words if not isStopWord(word)]   #stopwords removal
    words = [stemming(word) for word in words]    #word stemming
    words = [word.lower() for word in words]    #lowercasing words
    return words


###### test snippet
if __name__ == '__main__':
    print isStopWord('ffff')
    print stemming('athletes')

    docs_list = []
    cf = CranFile ('../CranfieldDataset/cran.all')   #preprocess all docs in the collection
    for doc in cf.docs:
        docs_list.append(splitDoc(doc))

#####
