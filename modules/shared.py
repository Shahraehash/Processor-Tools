from flask import Blueprint, current_app, jsonify, request, make_response, abort
import pandas as pd
import numpy as np
import os
import time

import uuid

from datetime import datetime
from tinydb import TinyDB, Query

#helper functions
from .helpers import convert_blanks_to_nan, find_nan_counts

db = TinyDB('db.json')

shared = Blueprint(
    'shared',
    __name__,
    url_prefix='/shared'
)


@shared.route('/data_file_upload',methods=["POST"])
def data_file_upload():

    file_obj = request.files['file']
    file_name = request.headers['X-filename'] #filename stored in special header
    file_group = request.headers['X-filegroup']

    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    storage_id = str(uuid.uuid4())

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

    #Script will try to read file and return data. If it fails it will delete
    #the file.
    try:
        df = pd.read_csv(file_path)

        #helper function to clean up nan rows
        df = convert_blanks_to_nan(df)
        #update file with cleaned up fields

        #trim column names
        df.columns = df.columns.str.replace(' ', '')

        df.to_csv(file_path, index=False)

        valid_data_types = ['int64','float64']
        invalid_columns = []

        for item in df.dtypes.keys():
            if df.dtypes[item] not in valid_data_types:
                invalid_columns.append(item)

        #params
        skew = df.skew()
        skew.name = 'skew'

        describe = df.describe().append(skew).transpose()
        describe.reset_index(inplace=True)
        describe = describe.rename(columns={'index':'feature'})
        describe = describe.round({
            'mean': 1,
            'std': 1,
            'min': 1,
            '25%': 1,
            '50%': 1,
            '75%': 1,
            'max': 1,
            'skew': 1
        })

        entry = {
        'user_id': 'ui000001',
        'storage_id': storage_id,
        'file_name':  file_name,
        'content_type': file_obj.content_type,
        'file_group': file_group, #training,testing,milo_results,train_test_split
        'upload_time': datetime.timestamp(datetime.now()),
        'rows': int(df.shape[0]),
        'columns': int(df.shape[1]),
        'column_names': list(df.columns.values),
        'column_names_reversed': list(np.flip(df.columns.values)),
        'nan_count': int(find_nan_counts(df)),
        'dtypes_count': df.dtypes.value_counts().to_json(),
        'nan_by_column': df.isna().sum().to_json(),
        'invalid_columns': list(invalid_columns),
        'describe': describe.to_json(orient="records")

        }
        db.insert(entry)

        response = make_response(
            jsonify(entry),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        time.sleep(1)
        return response

    except Exception as e:
        os.remove(file_path)
        return abort(500)

@shared.route('/milo_report_file_upload',methods=["POST"]) # The method should be consistent with the front end
def milo_report_file_upload():

    file_obj = request.files['file']  # Get files in Flask
    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    #save document
    storage_id = str(uuid.uuid4())
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)
    milo_data = pd.read_csv(file_path)

    milo_data['selected_features'] = milo_data['selected_features'].apply(lambda x: sorted(x.replace(" ","").replace("'","")[1:-1].split(',')))
    milo_data['length'] = milo_data['selected_features'].apply(lambda x: len(x))
    milo_data['selected_features'] = milo_data['selected_features'].apply(lambda x: str(x))
    milo_data['selected_features'] = milo_data['selected_features'].apply(lambda x: x.replace("'", '"'))

    #remove random forest
    rf_filter = milo_data['feature_selector'].str.contains("random forest", case=False)
    milo_data = milo_data[~rf_filter]

    #select only needed columns
    milo_data_reduced = milo_data[['feature_selector', 'selected_features', 'length']]

    #remove any options that preserve all columns
    no_full_columns = milo_data_reduced[milo_data_reduced['length'] < milo_data_reduced.length.max()]

    #prepare output
    result = no_full_columns.drop_duplicates().sort_values(by='feature_selector').set_index('feature_selector')
    final = result[~result.index.duplicated()]

    response = make_response(
        jsonify({
            "result": final.to_json(),
        }),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    time.sleep(1)
    return response

@shared.route('/validate_target_column',methods=["POST"])
def validate_target_column():
    target = request.json['target']
    storage_id = request.json['storage_id']

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)

    #count how many unique values are in the target column
    unique_values = len(df[target].value_counts())

    validation = True

    if unique_values != 2:
        validation = False

    response = make_response(
        jsonify({
            "validation": validation,
        }),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response
