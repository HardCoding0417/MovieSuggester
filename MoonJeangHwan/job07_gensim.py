import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('../data/cleaned_one_reviews.csv')
df_review.info()

reviews = list(df_review['reviews'])
print(reviews[0])

# 토큰단위로 분리
tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=20, workers=14, epochs=100, sg=1)
# 차원의 저주를 피하기 위해 100차원으로 줄임
# 출현빈도가 20번 이하면 학습 x
# cpu 코어를 8개 사용









