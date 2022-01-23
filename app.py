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
