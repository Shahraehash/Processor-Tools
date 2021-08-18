#'FLASK_APP=app.py FLASK_ENV=development flask run'
#docker run -d -p 5000:5000 fennell/ml-pp:latest

from flask import Flask, render_template, g, jsonify, request, redirect, url_for, session, flash, make_response, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import time

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

app.config['SECRET_KEY'] = 'mysecret'
app.config['firstConnect'] = False
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

#socketio
socketio = SocketIO(app, logger=True, engineio_logger=True)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

training_data = ''
testing_data = ''
milo_data = ''

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/')
def home():
    clearFiles()
    return render_template("index.html")

#Train Test Split Tools
@app.route('/train_test_split/upload',methods=["POST"])
def train_test_split_upload():

    file_obj = request.files['file']
    file_name = request.headers['X-filename']

    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    storage_id = str(uuid.uuid4())

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)


    df = pd.read_csv(file_path)
    rows = df.shape[0]
    columns = df.shape[1]
    column_names = list(df.columns.values)

    entry = {
    'user_id': 'ui000001',
    'storage_id': storage_id,
    'file_name':  file_name,
    'content_type': file_obj.content_type,
    'file_group': 'train_test_split', #training,testing,milo_results,train_test_split
    'upload_time': datetime.timestamp(datetime.now()),
    'rows': rows,
    'columns': columns,
    'column_names': column_names
    }

    db.insert(entry)

    return jsonify(entry)




@app.route('/train_test_split/metadata',methods=["POST"])
def train_test_split_metadata():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.json['storage_id'])
    df = pd.read_csv(file_path)

    target_column = request.json['target_column']
    #new code
    class_counts = df[target_column].value_counts()
    total_count = class_counts.sum()
    prevalence = class_counts[1] / total_count

    minority_class = 1

    if (class_counts[0] < class_counts[1]):
        minority_class = 0

    training_class_sample_size = 0

    minority_half = int(round(class_counts[minority_class]/2))

    if minority_half < 50:
        training_class_sample_size = 50
    else:
        training_class_sample_size = minority_half

    result = {
        'class_counts': class_counts.to_json(),
        'total_count': int(total_count),
        'prevalence': float(prevalence),
        'minority_class': int(minority_class),
        'training_class_sample_size': int(training_class_sample_size)
    }
    return jsonify(result)

@app.route('/train_test_split/process',methods=["POST"])
def train_test_split_process():

    return 'nothing'



@app.route('/data_upload',methods=["POST"]) # The method should be consistent with the front end
def upload():
    global training_data
    global testing_data
    global milo_data

    inbound_file = request.headers.get('X-inbound')
    file_obj = request.files['file']  # Get files in Flask
    if file_obj is None:
        # Indicates that no file was sent
        return "File not uploaded"

    if (inbound_file == 'training_data'):

    #save document
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "training_data.csv")
        file_obj.save(file_path)
        training_data = pd.read_csv(file_path)

        ##clean up column names
        training_data.columns = training_data.columns.str.replace(' ', '')

        rows = training_data.shape[0]
        columns = training_data.shape[1]
        column_names = training_data.columns.values.tolist()

        response = make_response(
            jsonify({
                "rows": rows,
                "columns": columns,
                "column_names": column_names
            }),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        time.sleep(1)
        return response


    if (inbound_file == 'testing_data'):

    #save document
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "testing_data.csv")
        file_obj.save(file_path)
        testing_data = pd.read_csv(file_path)

        ##clean up column names
        testing_data.columns = testing_data.columns.str.replace(' ', '')

        rows = testing_data.shape[0]
        columns = testing_data.shape[1]
        column_names = testing_data.columns.values.tolist()

        response = make_response(
            jsonify({
                "rows": rows,
                "columns": columns,
                "column_names": column_names
            }),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        time.sleep(1)
        return response

    if (inbound_file == 'milo_file'):

    #save document
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "milo_file.csv")
        file_obj.save(file_path)
        milo_data = pd.read_csv(file_path)

        milo_data['selected_features'] = milo_data['selected_features'].apply(lambda x: sorted(x.replace(" ","").replace("'","")[1:-1].split(',')))
        milo_data['length'] = milo_data['selected_features'].apply(lambda x: len(x))
        milo_data['selected_features'] = milo_data['selected_features'].apply(lambda x: str(x))
        milo_data['selected_features'] = milo_data['selected_features'].apply(lambda x: x.replace("'", '"'))
        df_red = milo_data[['feature_selector', 'selected_features', 'length']]

        test = df_red[df_red['length'] < df_red.length.max()]
        result = test.drop_duplicates().sort_values(by='feature_selector').set_index('feature_selector')
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





    else:
        return None

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
        clearFiles()
        return render_template('index.html')
    except Exception as e:
        print(e)
        print('change')
        return str(e)

@socketio.on('connect')
def handleMessage():
    print ("# User Connected ...")

@socketio.on('custom')
def render():
    global df
    time.sleep(4)
    emit('customEmit', str(df))



def clearFiles():
    print('clear files')
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))


# port = os.getenv('PORT', '5006')
# if __name__ == "__main__":
# 	app.run(host='0.0.0.0', port=int(port),debug=True)
#     #serve(app, url_scheme='http', threads=4, port=int(port))

if __name__ == '__main__':
    socketio.run(app)
    print('RUNNING')
    print('laksjhdfkjsdfkjshdf')
