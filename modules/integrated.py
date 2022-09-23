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
    params['rows'] = int(df.shape[0])
    params['nanRows'] = int(df[df.isna().any(axis=1)].shape[0])
    params['nanCells'] = int(df.isna().sum().sum())
    params['valueCells'] = int(df.count().sum())
    params['nanPercent'] = float(round(params['nanCells'] / (params['valueCells'] + params['nanCells']), 7) * 100)
    nanByColumn = df.isna().sum()
    params['nanByColumn'] = nanByColumn[nanByColumn != 0].to_dict()
    nanByColumnPercent = round(df.isna().sum() / df.shape[0] * 100, 5)
    params['nanByColumnPercent'] = nanByColumnPercent[nanByColumnPercent !=0].to_dict()
    params['columns'] = int(df.shape[1])
    params['columnNames'] = list(df.columns.values)
    params['columnNamesReverse'] = list(df.columns.values).reverse()
    params['describe'] = df.describe().to_dict()

    return params


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