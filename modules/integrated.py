from flask import Blueprint, current_app, jsonify, request, make_response, abort
import pandas as pd
import numpy as np
import os
import simplejson

import uuid

from datetime import datetime
from tinydb import TinyDB

#helper functions
from .helpers import convert_blanks_to_nan, find_nan_counts

db = TinyDB('db.json')

integrated = Blueprint(
    'integrated',
    __name__,
    url_prefix='/integrated'
)




def file_params(df):
    params = {}
    #size
    params['size'] = {}
    params['size']['rows'] = int(df.shape[0])
    params['size']['cols'] = int(df.shape[1])

    #missing values
    params['missing'] = {}
    ##rows
    params['missing']['rows'] = int(df[df.isna().any(axis=1)].shape[0])
    params['missing']['rowsPercent'] = float(round(params['missing']['rows'] / params['size']['rows'], 7) * 100)
    ##cells
    params['missing']['cells'] = int(df.isna().sum().sum())
    params['missing']['cellsPercent'] = float(round(params['missing']['cells'] / (params['size']['rows'] * params['size']['cols']), 7) * 100)
 
    #names
    params['names'] = {}
    params['names']['cols'] = list(df.columns.values)
    params['names']['colsReverse'] = list(df.columns.values)
    params['names']['colsReverse'].reverse()

    #describe
    params['describe'] = df.describe().to_dict()

    return params


def int_list_to_string(lst):
    return list(map(lambda n: str(n), lst))




def file_validation(fileObjectArray, target):
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
                        'misisng': z['storageId'],
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
        'mismatchedColumns': mismatchedColumns
    }

    return validation




def save_file(file_obj, storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

def load_file(storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)
    #Automatic fixes
    df = df.replace(r'^\s*$', np.nan, regex=True) #replaces empty strings spacess with NaN
    return df

@integrated.route('/store',methods=['POST'])
def integrated_store():

    files = request.files.getlist('files')
    for file in files:
        storage_id = str(uuid.uuid4())
        d = {
            'name' : file.filename,
            'storageId' : storage_id
            }
        save_file(file, storage_id)

    response = make_response(
        simplejson.dumps(d, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response    


@integrated.route('/params',methods=['POST'])
def integrated_params():
    storage_id = request.json['storageId']
    name = request.json['name']
    df = load_file(storage_id)
    params = file_params(df)
    #maintain storageId
    params['storageId'] = storage_id
    params['name'] = name

    response = make_response(
        simplejson.dumps(params, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response    


@integrated.route('/validate',methods=['POST'])
def integrated_validate():
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']


    validation = file_validation(fileObjectArray, target)


    response = make_response(
        simplejson.dumps(validation, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response


@integrated.route('/transform/',methods=['POST'])
def integrated_transform():
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']
    transform = request.json['transform']

    output_array = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])


        #define transforms

        if transform['type'] == 'targetMap':

            df = transform_target_map(df, target, transform)


        storage_id = str(uuid.uuid4())
        storage_file = df.to_csv(index=False)
        df.to_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id), index=False)

        params = file_params(df)
        params['storageId'] = storage_id
        params['name'] = file['name']


        output_array.append(params)

    response = make_response(
        simplejson.dumps(output_array, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response   
    

@integrated.route('/analyze/',methods=['POST'])
def integrated_analyze():
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']
    analyze = request.json['analyze']

    df_array = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])   

        df_array.append(df)

    df = pd.concat(df_array)

    result = analyze_missing_columns(df, target)

    json = {'fileAnalysisCombined': result}

    response = make_response(
        simplejson.dumps(json, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response       



@integrated.route('/effect/column_removal',methods=['POST'])
def integrated_effect_column_removal():
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']
    effect = request.json['effect']

    result = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])  

        r = effect_column_removal(df, target, effect) 

        result.append(r)
        

    json = {'fileEffectArray': result}

    response = make_response(
        simplejson.dumps(json, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response      





#ANALYSIS
def analyze_missing_columns(df, target):

    df.drop(target, axis=1, inplace=True)
    
    missing = []

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
        d['percentContributions'] = round(d['total'] / df.isnull().sum().sum() * 100, 2)
        d['col'] = col

        if d['total'] > 0:
            d = d.to_dict()
            missing.append(d)

    return missing


#EFFECTS
def effect_column_removal(df, target, effect):
    
    df_drop = df.drop(effect['selectedColumns'], axis=1)



    return {
        'old': file_params(df),
        'new': file_params(df_drop)
    }


##TRANSFORMS

def transform_target_map(df, target, transform):
    df[target] = df[target].astype('str').map(transform['data']['map']).astype('int')
    return df