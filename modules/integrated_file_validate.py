


from flask import Blueprint, current_app, jsonify, request, make_response, abort
import pandas as pd
import numpy as np
import os
import uuid

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params, create_binary_map

#ANALYSIS

#rules to detect potential errors in data
def check_df_size(df, target):

    df_missing = df[df.isna().any(axis=1)]
    df_non_missing = df.drop(df_missing.index)


    #constructs a list of value counts for the various dfs for front end use
    table_df = pd.DataFrame([
        df[target].value_counts(),
        df_missing[target].value_counts(),
        df_non_missing[target].value_counts()

    ]).fillna(0).transpose()
    
    table_df.columns = ['total', 'missing', 'complete']
    table = table_df.to_dict(orient='index')


    result = {}

    result['rowsCount'] = int(df.shape[0])
    result['rowsCompleteCount'] = int(df_non_missing.shape[0])
    result['rowsMissingCount'] = int(df_missing.shape[0])
    result['rowMissingPercent'] = float(df_missing.shape[0] / df.shape[0])
    result['classMin'] = minClassSize(df, target)
    result['classCompleteMin'] = minClassSize(df_non_missing, target)
    result['table'] = table

    return result
            
# Special method to ensure value counts always return value 
# even if a sub-dataframe ends up being empty
def minClassSize(df, target):
    value_counts = df[target].value_counts()
    if len(value_counts > 1):
        return int(value_counts.min())
    else:
        return 0
               






def analysis_file_validate(fileObjectArray, target):

    size_checks = []

    for i, file in enumerate(fileObjectArray):
        df = load_file(file['storageId'])
        size_checks.append(check_df_size(df, target))

    individual_file_validation = []

    for i, file in enumerate(fileObjectArray):
        checklist = {
            'hasTarget': False,
            'targetValues': None,
            'targetCount': None,
        }

        #check for target column
        has_target = target in file['names']['cols']
        if has_target:
            checklist['hasTarget'] = True

            df = load_file(file['storageId'])
            target_values = list(df[target].unique())
            target_count = len(target_values)
            checklist['targetValues'] = int_list_to_string(target_values)
            checklist['targetCount'] = target_count
        
        individual_file_validation.append(checklist)
        
    #All target values
    all_target_values = []

    for result in individual_file_validation:
        if result['hasTarget']:
            all_target_values.append(result['targetValues'])
    
   
    r = np.array(all_target_values).flatten()
    unique_target_values = int_list_to_string(list(np.unique(r)))
    unique_target_values.sort()
    value_map = create_binary_map(unique_target_values)
    #mismatched columns
    mismatchedColumns = []

    for z in fileObjectArray:
        for y in fileObjectArray:
            if z['storageId'] != y['storageId']:
                comp = [x for x in y['names']['cols'] if x not in z['names']['cols']]
                if len(comp) > 0:
                    mismatchedColumns.append({
                        'has': y['storageId'],
                        'hasName': y['name'],
                        'misisng': z['storageId'],
                        'missingName': z['name'],
                        'missingCols': comp
                    })


    #evaluate file data for validity

    valid_array = []
    for result in individual_file_validation:
        #check if target present
        valid_array.append(True) if result['hasTarget'] else valid_array.append(False)
        #ensure at least 2 values per file (support multi-class)
        valid_array.append(True) if result['targetCount'] >= 2 else valid_array.append(False)
    
    #check if all target values are consistent (at least 2 classes for classification)
    valid_array.append(True) if len(unique_target_values) >= 2 else valid_array.append(False)
    #check if all files have the same columns
    valid_array.append(True) if len(mismatchedColumns) == 0 else valid_array.append(False)



    validation = { 
        'valid': all(valid_array), #use all() to check if all values are true
        'targetMap': value_map,
        'individualValidation': individual_file_validation,
        'allTargetValues': unique_target_values,
        'mismatchedColumns': mismatchedColumns,
        'sizeChecks': size_checks
    }

    return validation

#EFFECT
#None

#TRANSFORM
def transform_file_validate_target_map(fileObjectArray, target, transform):

    result = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])

        df[target] = df[target].astype('str').map(transform['data']['map']).astype('int')
        #store file and generate file object
        result.append(store_file_and_params(df, file['name'], file['type']))

    return result
