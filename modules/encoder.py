from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import os
import uuid
from datetime import datetime
import simplejson
from sklearn.preprocessing import OneHotEncoder

#helper functions
from .helpers import convert_blanks_to_nan, find_nan_counts

encoder = Blueprint(
    'encoder',
    __name__,
    url_prefix='/encoder'
)



def save_file(file_obj, storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

def load_file(storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)
    df_nan = df[df.isna().any(axis=1)]
    df_remove_nan = df.drop(df_nan.index)
    return {
        'df_remove_nan': df_remove_nan,
        'df_nan': df_nan
    }

def find_invalid_columns(df):
    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    valid = df.select_dtypes(include=valid_data_types)
    
    invalid = df.drop(columns=valid.columns)
    
    invalid_columns = []
    
    for column in invalid.columns:
        uniq = list(invalid[column].unique())

        invalid_columns.append(
        {
            'name': column,
            'values': uniq, #Do this better, right now need to cover if bool
            'type': str(invalid[column].dtype),
            'count': len(invalid[column].unique())
        })

    return invalid_columns




@encoder.route('/dummy_encode_non_numerical_columns',methods=['POST'])
def dummy_encode_non_numerical_columns():

    storage_id = request.json['storage_id']

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)

    df = pd.read_csv(file_path)

    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

    valid = df.select_dtypes(include=valid_data_types)
    invalid = df.drop(columns=valid.columns)

    invalid_columns = []
    for column in invalid.columns:
        uniq = list(invalid[column].unique())

        invalid_columns.append(
        {
            'name': column,
            'values': uniq,
            'type': str(invalid[column].dtype),
            'count': len(invalid[column].unique())
        })

    column_map = [] #track mapping of columns
    for col_data in invalid_columns:
        
        #Ensure Boolean Values are Preserved
        if col_data['type'] == 'bool':
            invalid[col_data['name']] = invalid[col_data['name']].astype('int')
        
        #Ensure Nonboolean Binary Variables are kept as a single column
        elif col_data['count'] == 2:
            mapping = {}
            for index, val in enumerate(col_data['values']):
                mapping[val] = index
            column_map.append({
                'column': col_data['name'],
                'map': mapping
            })
            invalid[col_data['name']] = invalid[col_data['name']].map(mapping).astype('int') 
        
        #Dummy encode
        elif col_data['count'] > 2:
            
            enc = OneHotEncoder(handle_unknown='ignore')
            
            #Need 2D vector to do the fit
            vector = invalid[col_data['name']].values.reshape(-1,1)
            enc.fit(vector)
            
            trans = enc.transform(vector).toarray()
            
            temp_df = pd.DataFrame(trans, columns=enc.categories_).add_prefix(col_data['name'] + '_').astype('int')
            
            #Adjust original columns
            invalid = pd.concat([temp_df,invalid], axis=1)
            invalid = invalid.drop(col_data['name'], axis=1)

    final_object = {
        'file': pd.concat([valid, invalid], axis=1).to_csv(index=False),
    }
    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(final_object, ignore_nan=True),
        # jsonify(final_object),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response




@encoder.route('/store',methods=['POST'])
def encoder_store():

    file_obj = request.files['file']
    filename = request.headers['filename'] #filename stored in special header
    target = request.headers['target']

    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    storage_id = str(uuid.uuid4())
    save_file(file_obj, storage_id)

    df = load_file(storage_id)
    nan_count = df['df_nan'].shape[0]
    df = df['df_remove_nan']

    #ensure all types in values array do not create error for JSON
    invalid_columns = find_invalid_columns(df)
    for item in invalid_columns:
        item['values'] = str(item['values'])

    metadata = {
    'user_id': 'temp',
    'storage_id': storage_id,
    'filename':  filename,
    'upload_time': datetime.timestamp(datetime.now()),
    'rows': int(df.shape[0]),
    'columns': int(df.shape[1]),
    'column_names': list(df.columns.values),
    'nan_count': nan_count,
    'target': target,
    'invalid_columns': list(invalid_columns),
    }

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(metadata, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response