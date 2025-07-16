
import pandas as pd
import numpy as np

from .helpers import load_file, save_file, file_params, store_file_and_params


#ANALYSIS
def analyze_column_removal(fileObjectArray, target):

    df_array = []

    for file in fileObjectArray:

        df = load_file(file['storageId'])   
        df_array.append(df)

    df = pd.concat(df_array)

    result = []

    #determine how to relabel groupings of booleans
    mapDict = {True: 'singleMissing', False: 'multipleMissing'}

    #calculate how many rows have single missing values
    #row_opporunities = (df[df.isnull().sum(axis=1) != 0].isnull().sum(axis=1) == 1).map(mapDict).value_counts()

    #determine metrics for each individula column
    for col in df.columns:

        #determine how many rows have single missing values vs multiple
        split = df[df[col].isna()].isna().sum(axis=1) > 1
        d = split.map(mapDict).value_counts() #group

        #complete dictionary
        if 'singleMissing' not in d:
            d['singleMissing'] = 0
        if 'multipleMissing' not in d:
            d['multipleMissing'] = 0

        #other metrics to use
        d['total'] = d.sum()
        d['percentValues'] = round(d['total'] / (df.shape[0] * df.shape[1]) * 100, 2)
        
        # Avoid division by zero when there are no null values
        total_null_values = df.isnull().sum().sum()
        if total_null_values > 0:
            d['percentContributions'] = round(d['total'] / total_null_values * 100, 2)
        else:
            d['percentContributions'] = 0.0
            
        d['col'] = col

        if d['total'] > 0:
            d = d.to_dict()
            result.append(d)
        result.sort(key=lambda x: x['percentContributions'], reverse=True) #sort by total missing values

    json = {'fileAnalysisCombined': result}

    return json


#EFFECT
def effect_column_removal(fileObjectArray, target, effect):

    result = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])      
        df_drop = df.drop(effect['selectedColumns'], axis=1)

        result.append({
            'old': file_params(df),
            'new': file_params(df_drop)
        })

    json = {'fileEffectArray': result}

    return json


#TRANSFORM
def transform_column_removal(fileObjectArray, target, transform):
    result = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])

        df.drop(transform['data']['selectedColumns'], axis=1, inplace=True)
        #store file and generate file object
        result.append(store_file_and_params(df, file['name'], file['type']))

    return result
