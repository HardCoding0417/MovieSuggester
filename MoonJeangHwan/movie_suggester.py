import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    moviIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[moviIdx, 0]
    return recMovieList

df_reviews = pd.read_csv('../data/cleaned_one_reviews.csv')
Tfidf_matrix = mmread('../models/Tfidf_movie_review.mtx').tocsr()

with open('../data/Tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

print(df_reviews.iloc[383,0])
cosine_sim = linear_kernel(Tfidf_matrix[383], Tfidf_matrix)
print(cosine_sim[0])
print(len(cosine_sim[0]))
recommendation = getRecommendation(cosine_sim)
print(recommendation)




