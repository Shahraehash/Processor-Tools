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
    ##columns
    missingColumn = df.isna().sum()
    params['missing']['cols'] = missingColumn[missingColumn != 0].to_dict()
    ###percent of total values in colums
    nanByColumnPercent = round(df.isna().sum() / df.sum().sum() * 100, 4)
    params['missing']['colsPercent'] = nanByColumnPercent[nanByColumnPercent !=0].to_dict()
    ###percent ot total missing values
    nanColumnContributionPercent = round(df.isna().sum() / df.isna().sum().sum() * 100, 2)
    params['missing']['colsPercentContribution'] = nanColumnContributionPercent[nanColumnContributionPercent !=0].to_dict()

    #names
    params['names'] = {}
    params['names']['cols'] = list(df.columns.values)
    params['names']['colsReverse'] = list(df.columns.values)
    params['names']['colsReverse'].reverse()

    #describe
    params['describe'] = df.describe().to_dict()

    return params


def file_validation(fileObjectArray, target):

    #check for missing target
    missingTarget = []
    for z in fileObjectArray:
        if not target in z['names']['cols']:
            missingTarget.append(z['storageId'])

    #check for number of values within target
    targetValuesArray = []
    for z in fileObjectArray:
        if not z['storageId'] in missingTarget:
            df = load_file(z['storageId'])
            targetValuesArray.append(df[target].unique())
    r = np.array(targetValuesArray).flatten()
    targetValues = list(np.unique(r))
    targetValues = list(map(lambda n: str(n), targetValues)) #convert to string for json serialisation

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


    validation = {
        'valid': len(missingTarget) == 0 and len(mismatchedColumns) == 0 and len(targetValues) == 2,
        'missingTarget': missingTarget,
        'mismatchedColumns': mismatchedColumns,
        'targetValues': targetValues
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