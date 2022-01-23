from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import numpy as np
import os
import time
import json
import simplejson

#helper functions
import preprocessor_modules.helpers as helpers

column_reducer = Blueprint(
    'column_reducer',
    __name__,
    url_prefix='/column_reducer'
)

@column_reducer.route('/build',methods=["POST"])
def build():
    storage_id = request.json['storage_id']
    selected_columns = request.json['selected_columns']
    target = request.json['target']

    #create single column list
    output_columns = selected_columns.copy()
    output_columns.append(target)

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)

    #Select on desired columns
    df = df[output_columns]

    missing = df[df.isna().any(axis=1)]
    df = df.drop(missing.index)

    final_data = {
        'output_file': df.to_csv(index=False),
        'missing_file': missing.to_csv(index=True, index_label="source_row"),
        'missing_count': int(missing.shape[0]),
        'column_count': int(df.shape[1])
    }

    time.sleep(2)

    return make_response(final_data)


@column_reducer.route('/milo_file_upload',methods=["POST"]) # The method should be consistent with the front end
def milo_file_upload():

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
