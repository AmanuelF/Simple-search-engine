

'''
Authors: Manas Gaur, Amanuel Alambo
Instructor: Dr. Keke Chen

Index structure:

    The Index class contains a list of IndexItems, stored in a dictionary type for easier access

    each IndexItem contains the term and a set of PostingItems

    each PostingItem contains a document ID and a list of positions that the term occurs

'''
import util
import doc

from collections import OrderedDict,defaultdict   #for dealing with sorting dictionaries based on keys or values---and a dictionary of lists
import math    
import cran  
import json 
import sys 

class Posting:
    def __init__(self, docID):
        self.docID = docID
        self.positions = []

    def append(self, pos):
        self.positions.append(pos)

    def sort(self):
        ''' sort positions'''
        self.positions.sort()

    def merge(self, positions):
        self.positions.extend(positions)

    def term_freq(self):
        ''' return the term frequency in the document'''
        #ToDo
        return len(self.positions)   #term frequency in a document is the length of the list of positions for a document


class IndexItem:
    def __init__(self, term):
        self.term = term
        self.posting = {}    #postings are stored in a python dict for easier index building
        self.sorted_postings= []      # may sort them by docID for easier query processing

    def add(self, docid, pos):
        ''' add a posting'''
        if not self.posting.has_key(docid):
            self.posting[docid] = Posting(docid)
        self.posting[docid].append(pos)

    def sort(self):
        ''' sort by document ID for more efficient merging. For each document also sort the positions'''
        # ToDo
        self.posting = OrderedDict(sorted(self.posting.items(), key=lambda t:t[0]))
        for docID,pos_list in self.posting.iteritems():
            self.posting[docID] = sorted(pos_list, reverse=False)


class InvertedIndex:

    def __init__(self):
        self.items = defaultdict(list) # list of IndexItems--this corresponds to a structure of the form {term-1:{doc-1:[pos-1,...,pos-n]},....}
        self.nDocs = 0  # the number of indexed documents


    def indexDoc(self, doc): # indexing a Document object
        ''' indexing a docuemnt, using the simple SPIMI algorithm, but no need to store blocks due to the small collection we are handling. Using save/load the whole index instead'''

        # ToDo: indexing only title and body; use some functions defined in util.py
        # (1) convert to lower cases,
        # (2) remove stopwords,
        # (3) stemming
        
        
        doc_tb = doc.title + doc.body   #concatenating the title and the body as we want to index just the title and the body
        words = util.splitDoc(doc_tb)   #call to util's splitDoc method which performs calls tokenizing, stemming, stopword removal, lowercasing and splitting

    
        #pos_list = list()
        for term in list(set(words)):   #iterating through the set of words of a document so a single word is iterated once
            term = str(term)    #conversion into a string
            term_positions = [i for i,val in enumerate(words) if val==term]   
            doc_dict = {}     #dictionary to store a document's docID as key and a term's position as value
            doc_dict[doc.docID] = term_positions    #term positions in a document
            if term not in list(self.items.keys()):    #condition to check presence of a key in a dict before appending a value
                self.items[term]=list()              #intializes a dictionary for a term if the term doesn't appear as a key in the dictionary
                self.items[term].append(doc_dict)     #a dictionary of docID as key and list of the positions of a term in a doc inserted to into items
            else:
                self.items[term].append(doc_dict)     #if term is present in the items dictionary the docID and term positions are appended

        self.nDocs += 1      #increments with each call to the method
        return self.items


    def sort(self):
        ''' sort all posting lists by docID'''
        #ToDo
        #sorting by posting lists by docID is handled in 'sort' method in class 'IndexItem' (a slight change to design)
    
    def find(self, term):
        return self.items[term]


    def save(self, filename):
        ''' save to disk'''
        # ToDo: using your preferred method to serialize/deserialize the index
        with open(filename, 'w') as f:
            json.dump(self.items, f, indent=4)     #json used for serializing
    
    def load(self, filename):
        ''' load from disk'''
        # ToDo
        with open(filename) as f:
            indexed_file = json.load(f)
        return indexed_file

    def idf(self, term):
        ''' compute the inverted document frequency for a given term'''
        #ToDo: return the IDF of the term
        idf_score = math.log(self.nDocs, len(self.items[term]))
        return idf_score

    # more methods if needed


def test():
    ''' test your code thoroughly. put the testing cases here'''
    II = InvertedIndex()   #InvertedIndex class instantiated
    index_loaded = II.load('test.json')   #loading an indexed file---name of the file passed should be the same name used in indexing and saving the file
    print type(index_loaded['four'])     #testing for example entry 'four'
    print (index_loaded['four'][0]) 
    
    print 'Pass'

def indexingCranfield():
    #ToDo: indexing the Cranfield dataset and save the index to a file
    # command line usage: "python index.py cran.all index_file"
    # the index is saved to index_file

    #input parameters from command line
    cran_file = sys.argv[1]     
    index_file = sys.argv[2]   

    cf = cran.CranFile(cran_file)  #instantiation of CranFile class

    II = InvertedIndex()   #InvertedIndex class instantiated
    dump=list()       #to store list of each doc to be indexed
    for doc in cf.docs:
        dump.append(II.indexDoc(doc))
    
    II.save(index_file)    #saves to an output file----call to 'save' method of 'InvertedIndex' class

    print 'Done'

if __name__ == '__main__':
    
    indexingCranfield()   #call to indexingCranfield method
    test()    #call to method 'test'

