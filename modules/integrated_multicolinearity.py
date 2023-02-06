
from flask import Blueprint, current_app, request, make_response
import simplejson
import pandas as pd
import numpy as np

from .helpers import load_file, save_file, file_params, store_file_and_params


#ANALYSIS
def analyze_multicolinearity(fileObjectArray, target):

    df_array = []

    for file in fileObjectArray:


        #only look at training and testing data without audit columns TODO better way of doing this
        if (file['type'] in ['train', 'test', 'combined']):
            df = load_file(file['storageId'])   
            df_array.append(df)

    df = pd.concat(df_array)

    #remove tracking columns for analysis
    df.drop(["origin_file_name", "origin_file_source_row"], axis=1, inplace=True)

    #remove target column
    df.drop(target, axis=1, inplace=True)


    correlation_mat = df.corr()
    correlation_mat = correlation_mat.round(2)

    #d3 heat map data structure
    d3 = []
    for ind in correlation_mat.index:

        for y,val in correlation_mat[ind].iteritems():
            obj = {}
            obj['x'] = ind
            obj['y'] = y
            obj['val'] = val

            d3.append(obj)    

    #List Data
    corr_pairs = correlation_mat.unstack()
    sorted_pairs = corr_pairs.sort_values(kind="quicksort", ascending=False)

    list_of_pairs = []

    for item in sorted_pairs.index:
        l = list(item)
        l.sort()
        if l[0] != l[1]:
            entry = {
                'features': l,
                'value': sorted_pairs[item]
            }
            if entry not in list_of_pairs:
                list_of_pairs.append(entry)


    final_object = {
        "list": list_of_pairs,
        "d3": d3, #data structure for d3 heatmap
        "cols": df.columns.tolist() #need to give list of columns without tracking columns to v-select
        #remove "origin_file_name", "origin_file_source_row" above
    }

    return final_object





#EFFECT
# no effect for this method


#TRANSFORM
def transform_multicolinearity(fileObjectArray, target, transform):
    result = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])

        df.drop(transform['data']['selectedColumns'], axis=1, inplace=True)
        #store file and generate file object
        result.append(store_file_and_params(df, file['name'], file['type']))

    return result    