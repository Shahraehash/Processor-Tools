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
    training_storage_id = request.json['training_storage_id']
    testing_storage_id = request.json['testing_storage_id']
    selected_columns = request.json['selected_columns']
    target_column = request.json['target_column']
    remove_nan_rows = request.json['remove_nan_rows']

    #create single column list
    output_columns = selected_columns.copy()
    output_columns.append(target_column)

    final_data = {
        'training': 'null',
        'testing': 'null',
        'training_missing': 'null',
        'testing_missing': 'null',
        'training_missing_count': 0,
        'testing_missing_count': 0
    }

    if (training_storage_id is not None):
        training_file = os.path.join(current_app.config['UPLOAD_FOLDER'], training_storage_id)
        training_data_df = pd.read_csv(training_file)

        #Select on desired columns
        training_data_df_reduced = training_data_df[output_columns]

        #Save as default output
        final_data['training'] = training_data_df_reduced.to_csv(index=False)

        #Check for missing rows
        training_missing = training_data_df_reduced[training_data_df_reduced.isna().any(axis=1)]
        training_missing_count = training_missing.shape[0]
        final_data['training_missing_count'] = training_missing_count

        #If front end dictates row removal and there are missing rows
        if (remove_nan_rows and training_missing_count > 0):

            #Include row index in export
            final_data['training_missing'] = training_missing.to_csv(index=True)

            #Update output and do not include row index
            training_data_df_reduced = training_data_df_reduced.drop(training_missing.index)
            final_data['training'] = training_data_df_reduced.to_csv(index=False)



    if (testing_storage_id is not None):
        testing_file = os.path.join(current_app.config['UPLOAD_FOLDER'], testing_storage_id)
        testing_data_df = pd.read_csv(testing_file)

        #Select on desired columns
        testing_data_df_reduced = testing_data_df[output_columns]

        #Save as default output
        final_data['testing'] = testing_data_df_reduced.to_csv(index=False)

        #Check for missing rows
        testing_missing = testing_data_df_reduced[testing_data_df_reduced.isna().any(axis=1)]
        testing_missing_count = testing_missing.shape[0]
        final_data['testing_missing_count'] = testing_missing_count

        #If front end dictates row removal and there are missing rows
        if (remove_nan_rows and testing_missing_count > 0):

            #Include row index in export
            final_data['testing_missing'] = testing_missing.to_csv(index=True)

            #Update output and do not include row index
            testing_data_df_reduced = testing_data_df_reduced.drop(testing_missing.index)
            final_data['training'] = testing_data_df_reduced.to_csv(index=False)

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
