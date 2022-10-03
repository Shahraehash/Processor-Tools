from flask import Blueprint, current_app, jsonify, request, make_response, abort
import pandas as pd
import numpy as np
import os
import simplejson

import uuid

from datetime import datetime
from tinydb import TinyDB

#helper functions
from .helpers import convert_blanks_to_nan, find_nan_counts, file_params

from .integrated_column_removal import analyze_column_removal, effect_column_removal

db = TinyDB('db.json')

integrated = Blueprint(
    'integrated',
    __name__,
    url_prefix='/integrated'
)







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

    #For Missing Columns
    if analyze['method'] == 'column_removal':
        json = analyze_column_removal(fileObjectArray, target)

    else: 
        json = {'error': 'invalid method'}

    response = make_response(
        simplejson.dumps(json, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response       



@integrated.route('/effect/',methods=['POST'])
def integrated_effect_column_removal():
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']
    effect = request.json['effect']

    if effect['method'] == 'column_removal':
        json = effect_column_removal(fileObjectArray, target, effect) 

    else: 
        json = {'error': 'invalid method'}
        
    response = make_response(
        simplejson.dumps(json, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response      







##TRANSFORMS

def transform_target_map(df, target, transform):
    df[target] = df[target].astype('str').map(transform['data']['map']).astype('int')
    return df