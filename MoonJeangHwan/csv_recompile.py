import pandas as pd
import re

df = pd.read_csv('2017-2018.csv')

df = re.sub(' ', title)
df = pd.DataFrame(list(titles), columns=["Title"])
df.to_csv(filename, index=False)


