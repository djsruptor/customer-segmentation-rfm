import pandas as pd 
import pycountry

def read_data(path):
    df = pd.read_csv(path)
    return df

def write_data(df, path):
    df.to_parquet(path, index=False)