#'FLASK_APP=app.py FLASK_ENV=development flask run'
#docker run -d -p 5000:5000 fennell/ml-pp:latest

from flask import Flask, render_template, g, jsonify, request, redirect, url_for, session, flash, make_response, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import time
import json

import simplejson

#Scikit learn
from sklearn.feature_selection import f_classif
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Make TinyDB
import uuid
from tinydb import TinyDB, Query
from datetime import datetime
db = TinyDB('db.json')



if not os.path.exists('files'):
    os.makedirs('files')

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
#Modules
from preprocessor_modules.parent_preprocessor import parent_preprocessor
app.register_blueprint(parent_preprocessor)

app.config['SECRET_KEY'] = 'mysecret'
app.config['firstConnect'] = False
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


training_data = ''
testing_data = ''
milo_data = ''


@app.route('/')
def home():
    #clearFiles()
    return render_template("index.html")


#TOOL SPECIFIC
#Column Reducer

@app.route('/column_reducer/process',methods=["POST"])
def column_reducer_process():
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
        training_file = os.path.join(app.config['UPLOAD_FOLDER'], training_storage_id)
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
        testing_file = os.path.join(app.config['UPLOAD_FOLDER'], testing_storage_id)
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






@app.route('/milo_file_upload',methods=["POST"]) # The method should be consistent with the front end
def upload():

    file_obj = request.files['file']  # Get files in Flask
    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    #save document
    storage_id = str(uuid.uuid4())
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
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



@app.route('/validate/target_column',methods=["POST"])
def validate_target_column():
    target = request.json['target']
    storage_id = request.json['storage_id']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
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






@app.route('/column_reducer/build_files',methods=["POST"])
def build_files():
    final_columns = request.json['finalColumns']
    has_testing_data = request.json['hasTestData']
    paths = {}

    training_save_path = os.path.join(app.config['UPLOAD_FOLDER'], "training_data_reduced.csv")
    testing_save_path = os.path.join(app.config['UPLOAD_FOLDER'], "testing_data_reduced.csv")


    training_data[final_columns].to_csv(training_save_path, index=False)
    paths['training'] = training_save_path

    if has_testing_data:
        print('build testing')
        testing_data[final_columns].to_csv(testing_save_path, index=False)
        paths['testing'] = testing_save_path

    return jsonify(paths)

@app.route('/column_reducer/training_reduced_file',methods=["POST"])
def return_training_reduced_file():
    try:
        return send_file(UPLOAD_FOLDER + "/training_data_reduced.csv", attachment_filename='training_data_reduced.csv', as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/column_reducer/testing_reduced_file',methods=["POST"])
def return_testing_reduced_file():
	try:
		return send_file(UPLOAD_FOLDER + "/testing_data_reduced.csv", attachment_filename='testing_data_reduced.csv', as_attachment=True)
	except Exception as e:
		return str(e)


@app.route('/return-files',methods=["GET"])
def return_files_tut():

	try:
		return jsonify(request)#send_file(UPLOAD_FOLDER + "/training_data.csv", attachment_filename='magic.csv', as_attachment=True)
	except Exception as e:
		return str(e)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    try:
        #clearFiles()
        return render_template('index.html')
    except Exception as e:
        print(e)
        print('change')
        return str(e)

def clearFiles():
    print('clear files')
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
