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
from .integrated_column_removal import analyze_column_removal, effect_column_removal



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

    response = make_response(
        simplejson.dumps(params, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response    


   

@integrated.route('/analyze/',methods=['POST'])
def integrated_analyze():
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']
    analyze = request.json['analyze']


    print(analyze['method'])


    #File Validate
    if analyze['method'] == 'file_validate':
        json = analysis_file_validate(fileObjectArray, target)

    #For Missing Columns
    elif analyze['method'] == 'column_removal':
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

    elif False:
        pass

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
    fileObjectArray = request.json['fileObjectArray']
    target = request.json['target']
    transform = request.json['transform']

    output_array = []

    for file in fileObjectArray:
        df = load_file(file['storageId'])


        #define transforms

        if transform['method'] == 'file_validate_target_map':

            df = transform_file_validate_target_map(df, target, transform)
        





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




##TRANSFORMS

