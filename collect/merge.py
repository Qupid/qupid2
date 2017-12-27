import pandas as pd

b = pd.read_csv("ft.csv")#labels
a = pd.read_csv("lab.csv")#features moet headers hebben
#merged = a.merge(b, on='url', how='inner')
merged = a.merge(b, on='url', how='inner')
#del merged['urlz']
print(merged)
#merged.to_csv("mjoined.csv", index=False)
