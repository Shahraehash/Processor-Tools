from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import os
import uuid
from datetime import datetime
import simplejson
from sklearn.preprocessing import OneHotEncoder

encoder = Blueprint(
    'encoder',
    __name__,
    url_prefix='/encoder'
)

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

    column_map = []
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

    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    storage_id = str(uuid.uuid4())

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

    #Script will try to read file and return data. If it fails it will delete
    #the file.
    # try:
    df = pd.read_csv(file_path)

    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    valid = df.select_dtypes(include=valid_data_types)
    invalid = df.drop(columns=valid.columns)
    invalid_columns = invalid.apply(lambda col: col.unique())

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
    'filename':  filename,
    'content_type': file_obj.content_type,
    'upload_time': datetime.timestamp(datetime.now()),
    'rows': int(df.shape[0]),
    'columns': int(df.shape[1]),
    'column_names': list(df.columns.values),
    'dtypes_count': df.dtypes.value_counts().to_json(),
    'nan_by_column': df.isna().sum().to_json(),
    'invalid_columns': invalid_columns.to_json(),
    'describe': describe.to_json(orient="records")
    }

    response = make_response(
        jsonify(entry),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response

    # except Exception as e:
    #
    #     os.remove(file_path)
    #     return abort(500)
