
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params


#ANALYSIS

def analyze_train_test_split_impute(fileObjectArray, target):
    df_array = []
    for file in fileObjectArray:

        df = load_file(file['storageId'])   
        df_array.append(df)

    df = pd.concat(df_array)

 

    return {'fileAnalysisCombined': result} 


#EFFECT
#none


#TRANSFORM
