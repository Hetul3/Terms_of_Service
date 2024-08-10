import pandas as pd
import glob

csv_files = glob.glob('Legal_Doc_Dataset/dataset*.csv')
print("Files found:", csv_files)

dfs = []

for file in csv_files:
    print("Reading file:", file)
    df = pd.read_csv(file, header=None, names=['text', 'classification'])
    
    df['text'] = df['text'].str.replace(r'^[\'"]+|[\'"]+$', '', regex=True).str.strip()
    dfs.append(df)
    
combined_dfs = pd.concat(dfs, ignore_index=True)

combined_dfs.to_csv('dataset.csv', index=False)