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


@app.route('/')
def home():
    #clearFiles()
    return render_template("index.html")



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
