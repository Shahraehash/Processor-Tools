import json
from json import load
from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import numpy as np
import os
import uuid
from datetime import datetime
import simplejson
from distutils import util
from sklearn.preprocessing import OneHotEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

#helper functions
from .helpers import convert_blanks_to_nan, find_nan_counts

encoder = Blueprint(
    'encoder',
    __name__,
    url_prefix='/encoder'
)

def remove_dotcsv(filename):
    return filename[:-4]

def transform_mixed_to_numeric(series):
    """
    Convert a series of mixed data types to numeric
    input: series
    """

    # non-numerics are converted to NaN and removed
    output = pd.to_numeric(series, errors='coerce')
    output = output.dropna()        

    return output

def transform_one_hot_encode(series):
    working = pd.Series(series)
    working = working.dropna()
    index = working.index
    
    enc = OneHotEncoder(handle_unknown='ignore')
    vector = working.values.reshape(-1,1)
    enc.fit(vector)
    trans = enc.transform(vector).toarray()
    output = pd.DataFrame(trans, columns=enc.categories_, index=index).add_prefix(series.name + '_').astype('int')
    
    return output

def transform_category_to_binary(series, map):
    return series.map(map).astype('int')

def save_file(file_obj, storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

def load_file(storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)
    #Automatic fixes
    df = df.replace(r'^\s*$', np.nan, regex=True) #replaces empty strings spacess with NaN
    return df


def define_invalid_columns(df):
    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'bool']

    valid = df.select_dtypes(include=valid_data_types)

    invalid = df.drop(columns=valid.columns)

    #process mixed data types
    transforms = {}

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
            #proposed_transform
            transforms[column] = {
                'type': 'mixed_to_numeric',
                'nan_row_index': list(col[col.isna() == True].index),
                'non_numeric_row_index': list(numeric[numeric == False].index)
            } 
        else:
            transforms[column] = {
                'type': 'one_hot_encode',
                'unique_values': list(col.unique()),
                'nan_row_index': list(col[col.isna() == True].index)
            }

            
    return transforms, list(invalid.columns)

def apply_column_transforms(dataframe, columns_to_remove, transforms, target, target_map):
    df = pd.DataFrame(dataframe)

    #Remove columns
    df = df.drop(columns=columns_to_remove)
    for column in columns_to_remove:
        if column in transforms:
            transforms.pop(column, None)

    for column in transforms:
        t = transforms[column]

        if t['type'] == 'mixed_to_numeric':
            df[column] = transform_mixed_to_numeric(df[column])

        elif t['type'] == 'category_to_binary':
            df[column] = transform_category_to_binary(df[column], t['map'])
        
        elif t['type'] == 'one_hot_encode':
            df = pd.concat([df, transform_one_hot_encode(df[column])], axis=1)
            df = df.drop(column, axis=1)

    try:
        df[target] = df[target].astype('str').map(target_map).astype('int')
    except:
        print('ERROR APPLYING TARGET MAP')

    #ensure target remains at end of file
    col_list = list(df.columns)
    i = col_list.index(target)
    reorder_list = col_list[:i] + col_list[i + 1:] + [target]
    df = df[reorder_list]
    return df 

def file_nan_metrics(df):
    output = {}
    nan_column_count = df.isnull().sum()
    nan_column_count = nan_column_count[nan_column_count > 0] #only if has NaN
    nan_column_count = nan_column_count.sort_values(ascending=False)

    output['nanByColumn'] = nan_column_count.to_json()
    output['rows'] = int(df.shape[0])
    output['nanRows'] = int(df[df.isna().any(axis=1)].shape[0])
    output['nanCells'] = int(df.isna().sum().sum())
    output['valueCells'] = int(df.count().sum())
    output['nanPercent'] = int(round(output['nanCells'] / (output['valueCells'] + output['nanCells']), 2) * 100)
    output['columns'] = int(df.shape[1])
    output['columnNames'] = list(df.columns.values)
    return output

@encoder.route('/apply_transforms',methods=['POST'])
def apply_transforms():
    
    result = {}

    target = request.headers['target']
    target_map = json.loads(request.headers['targetMap'])
    columns_to_remove = json.loads(request.headers['columnsToRemove'])
    
    print(request.json)
    files = request.json
    for file in files:
        result[file['name']] = {} #create file object for original and transform
       
        df = load_file(file['storageId'])

        result[file['name']]['original'] = file_nan_metrics(df) #original file

        transforms = file['invalidColumnsTransforms']

        df = apply_column_transforms(df, columns_to_remove, transforms, target, target_map)

        result[file['name']]['transform'] = file_nan_metrics(df)

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(result, ignore_nan=True),
        # jsonify(final_object),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response

@encoder.route('/manage_rows',methods=['POST'])
def manage_rows():
    
    output_files = {}

    target = request.headers['target']
    target_map = json.loads(request.headers['targetMap'])
    row_option = request.headers['rowOption']
    include_indexes = request.headers['includeIndexes']
    include_indexes = bool(util.strtobool(include_indexes))
    columns_to_remove = json.loads(request.headers['columnsToRemove'])

    files = request.json
    for file in files:

        df = load_file(file['storageId'])
        transforms = file['invalidColumnsTransforms']
        df = apply_column_transforms(df, columns_to_remove, transforms, target, target_map)
 

        print(row_option, 'row option')

        if (row_option == '0'):
            #change index to match excel
            df.index = df.index + 2 
            #change            
            missing = df[df.isna().any(axis=1)]
            output = df.drop(missing.index)
            if missing.shape[0] > 0:         
                output_files['Nan_rows_' + remove_dotcsv(file['name']) + '.csv'] = missing.to_csv(index=True, index_label="source_row")
                output_files[remove_dotcsv(file['name']) + '_encoded_NaN_removed' + '.csv'] = output.to_csv(index=include_indexes, index_label="source_row")
            else:
                output_files[remove_dotcsv(file['name']) + '_encoded' + '.csv'] = output.to_csv(index=include_indexes, index_label="source_row")

        elif (row_option == '1'):
            imp_mean = IterativeImputer(random_state=0)
            X = df.drop(columns=[target])
            y = df[target]

            #check if negative values exist in each column before imputation
            col_has_negative = ((X < 0).any()).to_dict()

            imp_mean.fit(X)
            result = pd.DataFrame(imp_mean.transform(X),columns=X.columns)
            result[df.columns[df.isna().any()]] = result[df.columns[df.isna().any()]].round(decimals=3)

            #if column does not have negative values, change all imputed negative values to 0
            for col in col_has_negative:
                if(not col_has_negative[col]):
                    column = result[col]
                    column[column < 0 ] = 0

            result[target] = y
            #change index to match excel
            result.index = result.index + 2 
            #change           
            output_files[remove_dotcsv(file['name']) + '_encoded_imputed' + '.csv'] = result.to_csv(index=include_indexes, index_label="source_row")

    result = {
        'files': output_files,
    }

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(result, ignore_nan=True),
        # jsonify(final_object),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response

#Method not actually used because part of initial metadata evaluation
@encoder.route('/evaluate_columns',methods=['POST'])
def evaluate_columns():
    files = request.json['files']

    output = {}

    for file in files:
        df = load_file(file['storageId'])
        transforms, invalid_columns = define_invalid_columns(df)
        output[file['name']] = {
            'invalid_columns': invalid_columns,
            'transforms': transforms
        }
    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(output, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response   


def store_files(files):
    '''
    Function used to store initial files to disk and generate storage Ids.
    '''
    storage_array = []

    for file in files:

        file_properties = {}

        #Name
        file_properties['name'] = file.filename
        
        #Storage Id
        storage_id = str(uuid.uuid4())
        file_properties['storageId'] = storage_id

        #Save file to disk
        save_file(file, storage_id) #custom helper function
        
        #Track
        storage_array.append(file_properties)

    return storage_array


def validate_target(df, target):
    '''
    Function used to validate target column. Removes NaN values.
    '''
    target_validation = {
        'validTarget': int(False), #for json
        'targetValues': [],
        'valuesCount': 0,
        'nanCount': 0
    }
    if target in df.columns.values:
        target_validation['nanCount'] = int(df[target].isna().sum())
        target_no_nan = df[target].dropna()
        target_validation['targetValues'] = list(target_no_nan.astype('str').unique())
        target_validation['targetValues'].sort()
        target_validation['valuesCount'] = int(len(target_validation['targetValues']))
        target_validation['validTarget'] = int(target_validation['valuesCount'] == 2)
    
    return target_validation
        

def file_params(df):
    params = {}
    params['rows'] = int(df.shape[0])
    params['nanRows'] = int(df[df.isna().any(axis=1)].shape[0])
    params['nanCells'] = int(df.isna().sum().sum())
    params['valueCells'] = int(df.count().sum())
    params['nanPercent'] = int(round(params['nanCells'] / (params['valueCells'] + params['nanCells']), 2) * 100)
    nanByColumn = df.isna().sum()
    params['nanByColumn'] = nanByColumn[nanByColumn != 0].to_dict()
    nanByColumnPercent = round(df.isna().sum() / df.shape[0] * 100, 1)
    params['nanByColumnPercent'] = nanByColumnPercent[nanByColumnPercent !=0].to_dict()
    params['columns'] = int(df.shape[1])
    params['columnNames'] = list(df.columns.values)
    params['describe'] = df.describe().to_dict()

    return params

@encoder.route('/store',methods=['POST'])
def encoder_store():

    target = request.headers['target']
    uploaded_files = request.files.getlist('files')

    #Object to store pipeline
    metadata = {
        'pipelineId': str(uuid.uuid4()),
        'upload_time': datetime.timestamp(datetime.now()),
    }

    #Each file is uploaded as part of a multipart form with the same key 'files
    #Saving process

    files = store_files(uploaded_files) #return Array of storageID, name, valid
    
    #Read saved files and extract metadata
    for file in files:
        try: 

            #File loading and validation
            df = load_file(file['storageId'])
            file['validFile'] = True

            #Target validation
            file['targetValidation'] = validate_target(df, target)

            #Transforms
            transforms, invalid_columns = define_invalid_columns(df.drop(columns=[target]))
            file['invalidColumns'] = invalid_columns
            file['invalidColumnsTransforms'] = transforms

            #File Metrics
            file['params'] = file_params(df)

        except Exception as e:
            print(e)
            file['validFile'] = False

    pipeline = {
        'metadata': metadata,
        'files': files
    }

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(pipeline, ignore_nan=True),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response    

