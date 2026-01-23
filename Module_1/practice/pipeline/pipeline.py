import sys 
import pandas as pd 

print("arguments" , sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({'day': [1, 2], 'num_passengers': [3, 4]})
df['month'] = month
print(df)
df.to_parquet(f'output_{month}.parquet',compression='gzip',index=False)
print(f"Parquet file saved for month {month}")