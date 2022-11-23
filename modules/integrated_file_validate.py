


from flask import Blueprint, current_app, jsonify, request, make_response, abort
import pandas as pd
import numpy as np
import os
import uuid

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params

#ANALYSIS

#rules to detect potential errors in data
def check_df(df, target, fileGroup):
    rows_max_training = 100000
    rows_max_testing = 100000
    cols_max = 1000
    missing_data_max = 0.5
    min_training_class_size = 25
    min_test_class_size = 10


    testing_size_valid = True
    training_size_valid = True
    total_size_valid = True
    rows_max_valid = True
    cols_max_valid = True

    df_missing = df[df.isna().any(axis=1)]

    missing_count = int(df_missing.shape[0])
    missing_percent = missing_count / df.shape[0]

    df_non_missing = df.drop(df_missing.index)

    if (fileGroup == 'combined'):
        testing_size_valid = all(df_non_missing[target].value_counts() > min_test_class_size)
        training_size_valid = all(df[target].value_counts() > min_training_class_size)
        total_size_valid = all(df[target].value_counts() > min_training_class_size + min_test_class_size)

        rows_max_valid = df.shape[0] < rows_max_training + rows_max_testing
        cols_max_valid = df.shape[1] < cols_max

    elif (fileGroup == 'train'):
        training_size_valid = all(df[target].value_counts() > min_training_class_size)

        rows_max_valid = df.shape[0] < rows_max_training
        cols_max_valid = df.shape[1] < cols_max        

    elif (fileGroup == 'test'):
        testing_size_valid = all(df_non_missing[target].value_counts() > min_test_class_size)

        rows_max_valid = df.shape[0] < rows_max_testing
        cols_max_valid = df.shape[1] < cols_max        

    return {
        'missing_count': missing_count,
        'missing_percent': missing_percent,
        'testing_size_valid': testing_size_valid,
        'training_size_valid': training_size_valid,
        'total_size_valid': total_size_valid,
        'rows_max_valid': rows_max_valid,
        'cols_max_valid': cols_max_valid,
        'all_valid': testing_size_valid and training_size_valid and total_size_valid and rows_max_valid and cols_max_valid
    }

def group_data(fileObjectArray, target):
    combined = []
    train = []
    test = []

    for file in fileObjectArray:
        if file['type'] == 'combined':
            combined.append(load_file(file['storageId']))
        elif file['type'] == 'train':
            train.append(load_file(file['storageId']))
        elif file['type'] == 'test':
            test.append(load_file(file['storageId']))
    
    if len(combined) > 0:
        df_combined = pd.concat(combined)

    else:
        df_combined = None

    if len(train) > 0:
        df_train = pd.concat(train)
    else:
        df_train = None

    if len(test) > 0:
        df_test = pd.concat(test)    
    else:
        df_test = None


    return {
        'combined': df_combined,
        'train': df_train,
        'test': df_train
    }



def analysis_file_validate(fileObjectArray, target):
    groups = group_data(fileObjectArray, target)

    group_results = {}

    for group in groups:
        if groups[group] is not None:
            r = check_df(groups[group], target, group)
            group_results[group] = r

    
    print("GROUP RESULTS",group_results, )

    individual_file_validation = []

    for file in fileObjectArray:
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

    value_map = {}
    for key, value in enumerate(unique_target_values):
        value_map[value] = key


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
        #ensure at least and only two values per file
        valid_array.append(True) if result['targetCount'] == 2 else valid_array.append(False)
    
    #check if all target value pairs are the same
    valid_array.append(True) if len(unique_target_values) == 2 else valid_array.append(False)
    #check if all files have the same columns
    valid_array.append(True) if len(mismatchedColumns) == 0 else valid_array.append(False)




    validation = { 
        'valid': all(valid_array), #use all() to check if all values are true
        'targetMap': value_map,
        'individualValidation': individual_file_validation,
        'allTargetValues': unique_target_values,
        'mismatchedColumns': mismatchedColumns,
        'groupResults': group_results
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


    



