import numpy as np
import pandas as pd

def convert_blanks_to_nan(df):
    return df.replace(r'^\s*$', np.nan, regex=True)

def find_nan_counts(df):
    return df[df.isna().any(axis=1)].shape[0]
