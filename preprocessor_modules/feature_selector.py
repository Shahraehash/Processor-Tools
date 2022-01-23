from flask import Blueprint, current_app, jsonify, request, make_response
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

#helper functions
import preprocessor_modules.helpers as helpers

feature_selector = Blueprint(
    'feature_selector',
    __name__,
    url_prefix='/feature_selector'
)

def calculate_percentile_columns(data_array, percentile):
  length = len(data_array)
  last_column = round(length * percentile/100)
  return data_array[0:last_column]

#Feature Selector
@feature_selector.route('/generate',methods=["POST"])
def generate():
    storage_id = request.json['storage_id']
    target = request.json['target']

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)

    ##remove missing files before calculating
    missing = df[df.isna().any(axis=1)]
    df = df.drop(missing.index)

    X = df.drop(columns=[target])
    y = df[target]
    feature_names = X.columns
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 5, stratify=y)


    #Select Percentile
    feature_scores = f_classif(X_train, y_train)[0]
    sorted_array_select_percentile = []

    for score, f_name in sorted(zip(feature_scores, feature_names), reverse=True):

        sorted_array_select_percentile.append({
            'feature': f_name,
            'score': round(score, 3)
        })

    #Random Forrest
    forest = RandomForestClassifier(random_state=0)
    rf_best = forest.fit(X_train, y_train)
    sorted_array_rf = []

    for score, f_name in sorted(zip(rf_best.feature_importances_, feature_names), reverse=True):
        sorted_array_rf.append({
            'feature': f_name,
            'score': round(score, 3)
        })

    #Calculate percentiles
    percentile_array = [100, 75, 50, 25]
    output_select_percentile = {}
    output_rf = {}

    for percentile in percentile_array:
        output_select_percentile[percentile] = calculate_percentile_columns(sorted_array_select_percentile, percentile)
        output_rf[percentile] = calculate_percentile_columns(sorted_array_rf, percentile)

    time.sleep(2)

    final_object = {
        'select_percentile': output_select_percentile,
        'rf': output_rf,
        'feature_number': len(output_rf)
    }

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(final_object, ignore_nan=True),
        # jsonify(final_object),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response


@feature_selector.route('/build',methods=["POST"])
def build():
    storage_id = request.json['storage_id']
    feature_selector_columns = request.json['feature_selector_columns']
    target = request.json['target']
    feature_selector_columns.append(target)

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)

    df = df[feature_selector_columns]

    #get missing data
    missing = df[df.isna().any(axis=1)]
    df = df.drop(missing.index)

    final_data = {
        'output_file': df.to_csv(index=False),
        'missing_file': missing.to_csv(index=True, index_label="source_row"),
        'missing_count': int(missing.shape[0]),
        'column_count': int(df.shape[1])
    }

    time.sleep(3)

    return make_response(final_data)
