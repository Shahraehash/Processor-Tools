from flask import Blueprint, current_app, request, make_response
import pandas as pd
import os
import time

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
