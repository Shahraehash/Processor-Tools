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

#helper functions
def convert_blanks_to_nan(df):
    return df.replace(r'^\s*$', np.nan, regex=True)

def find_nan_counts(df):
    return df[df.isna().any(axis=1)].shape[0]


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/')
def home():
    #clearFiles()
    return render_template("index.html")

@app.route('/query/all_files',methods=["POST"])
def query_all_files():

    query = db.all()

    response = make_response(
        jsonify(query),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    time.sleep(1)
    return response


#Train Test Split Tools


@app.route('/train_test_split/metadata',methods=["POST"])
def train_test_split_metadata():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.json['storage_id'])
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

@app.route('/train_test_split/process',methods=["POST"])
def train_test_split_process():
    storage_id = request.json['storage_id']
    target_column = request.json['target_column']
    training_class_sample_size = request.json['training_class_sample_size']
    prevalence_option = request.json['prevalence_option']
    majority_class = request.json['majority_class']
    extra = request.json['extra']
    include_index = request.json['include_index']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
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

    time.sleep(3)

    return make_response(final_data)

@app.route('/data_file_upload',methods=["POST"])
def data_file_upload():

    file_obj = request.files['file']
    file_name = request.headers['X-filename'] #filename stored in special header
    file_group = request.headers['X-filegroup']

    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    storage_id = str(uuid.uuid4())

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

    #Script will try to read file and return data. If it fails it will delete
    #the file.
    try:
        df = pd.read_csv(file_path)

        #helper function to clean up nan rows
        df = convert_blanks_to_nan(df)
        #update file with cleaned up fields

        #trim column names
        df.columns = df.columns.str.replace(' ', '')

        df.to_csv(file_path, index=False)

        valid_data_types = ['int64','float64']
        invalid_columns = []

        for item in df.dtypes.keys():
            if df.dtypes[item] not in valid_data_types:
                invalid_columns.append(item)

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
        'file_name':  file_name,
        'content_type': file_obj.content_type,
        'file_group': file_group, #training,testing,milo_results,train_test_split
        'upload_time': datetime.timestamp(datetime.now()),
        'rows': int(df.shape[0]),
        'columns': int(df.shape[1]),
        'column_names': list(df.columns.values),
        'column_names_reversed': list(np.flip(df.columns.values)),
        'nan_count': int(find_nan_counts(df)),
        'dtypes_count': json.loads(df.dtypes.value_counts().to_json()),
        'nan_by_column': json.loads(df.isna().sum().to_json()),
        'invalid_columns': list(invalid_columns),
        'describe': describe.to_json(orient="records")

        }

        db.insert(entry)

        response = make_response(
            jsonify(entry),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        time.sleep(1)
        return response

    except Exception as e:

        os.remove(file_path)
        return abort(500)

#TOOL SPECIFIC
#Correlation Tool
@app.route('/calc/cor',methods=["POST"])
def calc_corr():
    storage_id = request.json['storage_id']
    target = request.json['target']
    file = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file)

    correlation_mat = df.corr()
    correlation_mat = correlation_mat.round(2)

    #Graph
    graph_series = []
    for ind in correlation_mat.index:
        obj = {}
        obj['name'] = ind
        obj['data'] = []
        for x,y in correlation_mat[ind].iteritems():
            obj['data'].append({
                'x':x,
                'y':y
            })
        graph_series.append(obj)

    #List Data
    corr_pairs = correlation_mat.unstack()
    sorted_pairs = corr_pairs.sort_values(kind="quicksort", ascending=False)

    list_of_pairs = []

    for item in sorted_pairs.index:
        l = list(item)
        l.sort()
        if l[0] != l[1]:
            entry = {
                'features': l,
                'value': sorted_pairs[item]
            }
            if entry not in list_of_pairs:
                list_of_pairs.append(entry)


    final_object = {
        "graph": graph_series,
        "list": list_of_pairs
    }

    response = make_response(
        #Added to transform nan items to null when sending JSON
        simplejson.dumps(final_object, ignore_nan=True),
        # jsonify(final_object),
        200,
    )
    response.headers["Content-Type"] = "application/json"

    return response



@app.route('/calc/cor/process',methods=["POST"])
def calc_corr_process():
    storage_id = request.json['storage_id']
    feature_removal_list = request.json['feature_removal_list']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)

    df = df.drop(columns=feature_removal_list)

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

#helper function to calculate percentiles
def calculate_percentile_columns(data_array, percentile):
  length = len(data_array)
  last_column = round(length * percentile/100)
  return data_array[0:last_column]

#Feature Selector
@app.route('/calc/feature_selector',methods=["POST"])
def calc_feature_selector():
    storage_id = request.json['storage_id']
    target = request.json['target']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
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


@app.route('/calc/feature_selector/process',methods=["POST"])
def calc_feature_selector_process():
    storage_id = request.json['storage_id']
    feature_selector_columns = request.json['feature_selector_columns']
    target = request.json['target']
    feature_selector_columns.append(target)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
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
