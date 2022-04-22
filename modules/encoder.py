from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import numpy as np
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
    #Automatic fixes
    df = df.replace(r'^\s*$', np.nan, regex=True) #replaces empty strings spacess with NaN
    return df


def find_invalid_columns(df):
    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    valid = df.select_dtypes(include=valid_data_types)
    
    invalid = df.drop(columns=valid.columns)

    for column in invalid.columns:
        col = invalid[column]
        total_size = col.shape[0]
        #convert the column to numeric and replace str with NaN
        numeric = pd.to_numeric(col, errors='coerce')   
        #see how many NaN values there are
        nan_bool = numeric.isna()
        nans = col[nan_bool]
        nans_size = nans.shape[0]
        #if there are less than 20% of the total size, we can assume column is numerical
        nan_percent = nans_size / total_size
        if nan_percent < 0.20:
            valid[column] = numeric
            invalid.drop(column, axis=1, inplace=True)
             
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

    return valid, invalid, invalid_columns;


def ex_invalid_columns(df):
    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'bool']

    valid = df.select_dtypes(include=valid_data_types)

    invalid = df.drop(columns=valid.columns)
    fix = pd.DataFrame()

    #process mixed data types
    comments = {}

    for column in invalid.columns:
        col = invalid[column]

        total_count = col.shape[0]
        nan_count = col.isna().sum()

        col = col.dropna()
        not_nan_count = col.shape[0]

        numeric = ~pd.to_numeric(col, errors='coerce').isna()
        numeric_count = numeric.sum()

        if (numeric_count / total_count) > 0.6:
            invalid[column] = pd.to_numeric(col, errors='coerce')
            comments[column] = f'More than 0.6 of data is numeric. {nan_count} dropped' 
        
        elif (len(col.unique()) == 2):
            mapping = {}
            for index, val in enumerate(col.unique()):
                mapping[val] = index
            invalid[column] = col.map(mapping).astype('int')
            comments[column] = f'Two unique values. {str(mapping)}'
    
        elif (len(col.unique()) > 2):
            comments[column] = 'Will be one hot encoded'
            

    return comments, list(invalid.columns)



@encoder.route('/dummy_encode_non_numerical_columns',methods=['POST'])
def dummy_encode_non_numerical_columns():

    storage_id = request.json['storage_id']

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)

    df = pd.read_csv(file_path)

    valid, invalid, invalid_columns = find_invalid_columns(df)

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

    #Object to store pipeline
    pipeline = {
        'pipelineId': str(uuid.uuid4()),
        'upload_time': datetime.timestamp(datetime.now()),
        'initialFiles': [],
        #'initialFilesValidation': None #TODO: Add validation
    }

    #Each file is uploaded as part of a multipart form with the same key 'files
    #Saving process
    files = request.files.getlist('files')
    for file in files:
        storage_id = str(uuid.uuid4())
        save_file(file, storage_id) #custom helper function
        pipeline['initialFiles'].append({   
            'storageId': storage_id,
            'name': file.filename,
        })
    
    #Read saved files and extract metadata
    for file in pipeline['initialFiles']:
        df = load_file(file['storageId'])
        comments, invalid_columns = ex_invalid_columns(df)
        file['invalidColumns'] = invalid_columns
        file['invalidColumnsComments'] = comments
        file['rows'] = int(df.shape[0])
        file['columns'] = int(df.shape[1])
        file['columnNames'] = list(df.columns.values)       

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(pipeline, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response    

