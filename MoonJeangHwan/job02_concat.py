# 팀장 지시:
# 연도별로 작업해서 합칠게요
# 컬럼명은 ['titles', 'reviews']로 통일하겠습니다
# 파일명은 reviews_{연도}.csv 로 하겠습니다
# 경민님이 2013-2015
# 재희님이 2016-2023 해주세요


import pandas as pd
import glob
import re

data_paths = glob.glob('../rawdata/*')
print(data_paths[:-5])

df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.info()
df.drop_duplicates(inplace=True)
df.info()

df.rename('titles', 'reviews') # 컬럼명 변경
df.drop_duplicates(inplace=True)

my_year = 2023
df.to_csv('../rawdata/reviews_{}.csv'.format(my_year), index=False)













