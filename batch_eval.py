'''
Authors: Manas Gaur, Amanuel Alambo
Instructor: Dr. Keke Chen

a program for evaluating the quality of search algorithms using the vector model

it runs over all queries in query.text and get the top 10 results,
and then qrels.text is used to compute the NDCG metric

usage:
    python batch_eval.py index_file query.text qrels.text n

    output is the average NDCG over all the queries for boolean model and vector model respectively.
	also compute the p-value of the two ranking results. 
'''
import metrics
import query
from scipy.stats import ttest_ind
import sys
import math

def eval():
	# ToDo
	idx_file = sys.argv[1]   #index file
	idx_file = idx_file

	q_text = sys.argv[2]   #query text
	q_text = q_text

	qrels = sys.argv[3]   #qrels file
	qrels = qrels

	n = sys.argv[4]   #qrels file
	n = int(n)    #typecasting into int, so it can be processed by downstream tasks with no complaint
	
	#n=2  #can test by hard-coding
	#bool_ndcg_scores = list()
	#vec_ndcg_scores = list()
	for i in range(1):
		bool_ndcg_score, vec_ndcg_score = query.to_ndcg(qrels, q_text, idx_file, 10, n)   
		
		#ndcg_scores.append(avg_ndcg_score)
		bool_ndcg_scores = [0.99 if math.isnan(e) else e for e in bool_ndcg_score]
		vec_ndcg_scores = [0.99 if math.isnan(e) else e for e in vec_ndcg_score]
		print bool_ndcg_scores
		print vec_ndcg_scores
		print ttest_ind(bool_ndcg_scores, vec_ndcg_scores)   #checking wilcoxon for the first two lists of ndcg_scores

	print 'Done'

if __name__ == '__main__':
    eval()
