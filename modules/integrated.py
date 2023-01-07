from flask import Blueprint, current_app, jsonify, request, make_response, abort
import pandas as pd
import numpy as np
import os
import simplejson

import uuid

from datetime import datetime
from tinydb import TinyDB

#helper functions
from .helpers import convert_blanks_to_nan, find_nan_counts, file_params, save_file, load_file

from .integrated_file_validate import analysis_file_validate, transform_file_validate_target_map
from .integrated_column_removal import analyze_column_removal, effect_column_removal, transform_column_removal
from .integrated_encode_nonnumeric import analyze_encode_nonnumeric, transform_encode_nonnumeric
from .integrated_train_test_split_impute import analyze_train_test_split_impute, effect_train_test_split_impute, transform_train_test_split_impute
from .integrated_multicolinearity import analyze_multicolinearity, transform_multicolinearity


db = TinyDB('db.json')

integrated = Blueprint(
    'integrated',
    __name__,
    url_prefix='/integrated'
)

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
    params['type'] = 'combined' #TODO: change to smarter rule


    #automatically label as train and test if in the names
    #NOTE: since calls are made one file at a time, we cannot
    #know if there are multiple files here.
    #As such, there's an override rule in the frontend node that
    #will change the type to 'combined' if there's onlye a single
    #file
    name_check = name.lower()
    train_check = 'train' in name_check
    test_check = 'test' in name_check
    if train_check and test_check:
        params['type'] = 'combined'
    elif train_check:
        params['type'] = 'train'
    elif test_check:
        params['type'] = 'test'


    response = make_response(
        simplejson.dumps(params, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response    


   

@integrated.route('/analyze/',methods=['POST'])
def integrated_analyze():
    try: 
        fileObjectArray = request.json['fileObjectArray']
        target = request.json['target']
        analyze = request.json['analyze']

        #File Validate
        if analyze['method'] == 'file_validate':
            json = analysis_file_validate(fileObjectArray, target)

        #For Missing Columns
        elif analyze['method'] == 'column_removal':
            json = analyze_column_removal(fileObjectArray, target)

        #For Non-Numeric Columns
        elif analyze['method'] == 'encode_nonnumeric':
            json = analyze_encode_nonnumeric(fileObjectArray, target)

        #For Train Test Impute
        elif analyze['method'] == 'train_test_split_impute':
            json = analyze_train_test_split_impute(fileObjectArray, target)

        #For Multicolinearity
        elif analyze['method'] == 'multicolinearity':
            json = analyze_multicolinearity(fileObjectArray, target)

        # else: 
        #     json = {'error': 'invalid method'}

        response = make_response(
            simplejson.dumps(json, ignore_nan=True),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        return response
    except Exception as e:
        response = make_response(
            simplejson.dumps({'error': str(e)}),
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

    elif effect['method'] == 'train_test_split_impute':
        json = effect_train_test_split_impute(fileObjectArray, target, effect)

    else: 
        json = {'error': 'invalid method'}
        
    response = make_response(
        simplejson.dumps(json, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response      


@integrated.route('/transform/',methods=['POST'])
def integrated_transform():
    try:
        fileObjectArray = request.json['fileObjectArray']
        target = request.json['target']
        transform = request.json['transform']


        if transform['method'] == 'file_validate_target_map':
            json = transform_file_validate_target_map(fileObjectArray, target, transform)

        elif transform['method'] == 'column_removal':
            json = transform_column_removal(fileObjectArray, target, transform)
            
        elif transform['method'] == 'encode_nonnumeric':
            json = transform_encode_nonnumeric(fileObjectArray, target, transform)
                
        elif transform['method'] == 'train_test_split_impute':
            json = transform_train_test_split_impute(fileObjectArray, target, transform)

        elif transform['method'] == 'multicolinearity':
            json = transform_multicolinearity(fileObjectArray, target, transform)

        response = make_response(
            simplejson.dumps(json, ignore_nan=True),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        return response      
             
    except Exception as e:
        response = make_response(
            simplejson.dumps({'error': str(e)}),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        return response
    




@integrated.route('/export/',methods=['POST'])
def integrated_export():
    fileObjectArray = request.json['fileObjectArray']

    json = []

    for fileObject in fileObjectArray:
        storage_id = fileObject['storageId']
        df = load_file(storage_id)

        #cleaning rules
        # for col_name in df.columns:
        #     if ('age' in col_name.lower()):
        #         df[col_name] = df[col_name].astype(int)

        json.append({
            'type': fileObject['type'],
            'audit': True, #value which tracks if that file has audit rows
            'name': fileObject['name'],
            'content': df.to_csv(index=False, index_label="source_row")
        })
        df = df.drop(['origin_file_name', 'origin_file_source_row'], axis=1)
        json.append({
            'type': fileObject['type'],
            'audit': False,            
            'name': fileObject['name'],
            'content': df.to_csv(index=False, index_label="source_row")
        })        
    response = make_response(
        simplejson.dumps(json, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response       
