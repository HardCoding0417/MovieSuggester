import pandas as pd

df = pd.read_csv('../data/cleaned_review.csv')
df.dropna(inplace=True)
df.info()

one_sentences = []
for title in df['title'].unique():
    temp = df[df['title'] == title]
    one_sentence = ' '.join(temp['cleaned_sentences'])  # sentences 컬럼을 모두 합친다
    one_sentences.append(one_sentence)

df_one = pd.DataFrame({'titles':df['title'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.info()
df_one.to_csv('../data/cleaned_one_reviews.csv', index=False)



