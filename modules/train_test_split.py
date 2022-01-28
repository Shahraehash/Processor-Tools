from flask import Blueprint, current_app, jsonify, request, make_response
import pandas as pd
import os
import json

#helper functions
from .helpers import find_nan_counts

train_test_split = Blueprint(
    'train_test_split',
    __name__,
    url_prefix='/train_test_split'
)

@train_test_split.route('/generate',methods=["POST"])
def generate():
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], request.json['storage_id'])
    df = pd.read_csv(file_path)

    target_column = request.json['target_column']
    #new code
    class_counts = df[target_column].value_counts()
    total_count = class_counts.sum()

    #default value
    nan_counts = {0:0, 1:0}
    nan_counts = json.dumps(nan_counts)

    if (find_nan_counts(df) > 0):
        nan_counts = df[df.isna().any(axis=1)][target_column].value_counts()
        #ensure all values carried to front end
        if not 1 in nan_counts:
            nan_counts[1] = 0
        if not 0 in nan_counts:
            nan_counts[0] = 0

        nan_counts = nan_counts.to_json()

    minority_class = 1
    majority_class = 0

    if (class_counts[0] < class_counts[1]):
        minority_class = 0
        majority_class = 1


    result = {
        'class_counts': class_counts.to_json(),
        'total_count': int(total_count),

        'minority_class': int(minority_class),
        'majority_class': int(majority_class),
        'nan_class_counts': nan_counts

    }
    return jsonify(result)

@train_test_split.route('/build',methods=["POST"])
def build():
    storage_id = request.json['storage_id']
    target_column = request.json['target_column']
    training_class_sample_size = request.json['training_class_sample_size']
    prevalence_option = request.json['prevalence_option']
    majority_class = request.json['majority_class']
    extra = request.json['extra']
    include_index = request.json['include_index']

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)



    #get missing data
    missing = df[df.isna().any(axis=1)]
    df = df.drop(missing.index)

    train_0 = df[df[target_column] == 0].sample(training_class_sample_size)
    train_1 = df[df[target_column] == 1].sample(training_class_sample_size)

    train_combine = pd.concat([train_0,train_1])

    test_filtered = df.drop(train_0.index).drop(train_1.index)

    final_data = {
        'training': train_combine.to_csv(index=include_index, index_label="source_row"),
        'testing': test_filtered.to_csv(index=include_index, index_label="source_row"),
        #Rows missing value export. Index should always be included.
        'nan': missing.to_csv(index=True, index_label="source_row")
    }



    if prevalence_option == 1:
        reduction = test_filtered[test_filtered[target_column] == majority_class].sample(extra)
        test_reduced = test_filtered.copy()
        test_reduced = test_reduced.drop(reduction.index)
        final_data['testing'] = test_reduced.to_csv(index=include_index)

        #Extra data export. Index should always be included.
        final_data['extra'] = reduction.to_csv(index=True, index_label="source_row")

    return make_response(final_data)
