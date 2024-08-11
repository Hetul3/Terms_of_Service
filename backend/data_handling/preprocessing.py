import pandas as pd
import glob

def combine_csv():
    csv_files = glob.glob('../Legal_Doc_Dataset/dataset*.csv')
    print("Files found:", csv_files)
    
    dfs = []
    
    for file in csv_files:
        print("Reading file:", file)
        df = pd.read_csv(file, header=None, names=['text', 'classification'])
        
        df['text'] = df['text'].str.replace(r'^[\'"]+|[\'"]+$', '', regex=True).str.strip()
        dfs.append(df)
        
    combined_dfs = pd.concat(dfs, ignore_index=True)
    combined_dfs.to_csv('../Legal_Doc_Dataset/dataset.csv', index=False)
    
    return "../Legal_Doc_Dataset/dataset.csv"