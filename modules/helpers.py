from flask import current_app
import pandas as pd
import numpy as np
import os
import uuid


def global_params():
    return {
        'min_training_class_size': 25,
    }

def convert_blanks_to_nan(df):
    return df.replace(r'^\s*$', np.nan, regex=True)

def find_nan_counts(df):
    return df[df.isna().any(axis=1)].shape[0]

def save_file(file_obj, storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    file_obj.save(file_path)

def load_file(storage_id):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id)
    df = pd.read_csv(file_path)
    #Automatic fixes
    df = df.replace(r'^\s*$', np.nan, regex=True) #replaces empty strings spacess with NaN
    return df

def int_list_to_string(lst):
    return list(map(lambda n: str(n), lst))

def file_params(df):
    params = {}
    
    # Check if DataFrame is empty
    if df.empty:
        return {
            'size': {'rows': 0, 'cols': 0},
            'missing': {'rows': 0, 'rowsPercent': 0.0, 'cells': 0, 'cellsPercent': 0.0},
            'names': {'cols': [], 'colsReverse': []},
            'describe': []
        }
    
    #size
    params['size'] = {}
    params['size']['rows'] = int(df.shape[0])
    params['size']['cols'] = int(df.shape[1])

    #missing values
    params['missing'] = {}
    ##rows
    params['missing']['rows'] = int(df[df.isna().any(axis=1)].shape[0])
    if params['size']['rows'] > 0:
        params['missing']['rowsPercent'] = float(round(params['missing']['rows'] / params['size']['rows'], 7) * 100)
    else:
        params['missing']['rowsPercent'] = 0.0
    ##cells
    params['missing']['cells'] = int(df.isna().sum().sum())
    total_cells = params['size']['rows'] * params['size']['cols']
    if total_cells > 0:
        params['missing']['cellsPercent'] = float(round(params['missing']['cells'] / total_cells, 7) * 100)
    else:
        params['missing']['cellsPercent'] = 0.0
 
    #names
    params['names'] = {}
    params['names']['cols'] = list(df.columns.values)
    params['names']['colsReverse'] = list(df.columns.values)
    params['names']['colsReverse'].reverse()

    #describe
    try:
        # Only process numeric columns for describe
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty and len(numeric_df.columns) > 0:
            skew = numeric_df.skew()
            skew.name = 'skew'

            describe = pd.concat([numeric_df.describe(), skew.to_frame().T]).transpose()
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
            params['describe'] = describe.to_dict(orient="records")
        else:
            params['describe'] = []
    except Exception as e:
        params['describe'] = []

    return params

def store_file_and_params(df, file_name, file_type):
    
    # Check if DataFrame is empty
    if df.empty:
        # Create a minimal CSV file for empty DataFrame
        storage_id = str(uuid.uuid4())
        # Create empty CSV with just headers if columns exist
        if len(df.columns) > 0:
            df.to_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id), index=False)
        else:
            # Create completely empty CSV
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id), 'w') as f:
                f.write('')
    else:
        storage_id = str(uuid.uuid4())
        df.to_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], storage_id), index=False)

    params = file_params(df)
    params['storageId'] = storage_id
    params['name'] = file_name
    params['type'] = file_type

    return params

#create a smart mapping for target column (supports both binary and multi-class)
def create_binary_map(unique_column_value_list):
    #list(df[column].unique())
    items = unique_column_value_list
    
    # Filter out NaN, None, empty string values, and string representations of NaN
    items = [item for item in items if pd.notna(item) and str(item).strip() != '' and str(item).lower() != 'nan']
    
    if not items:  # If no valid items after filtering
        return {}
        
    items.sort()

    # If already numeric and sequential, use as-is
    if all(isinstance(item, (int, float)) or str(item).isdigit() for item in items):
        try:
            numeric_items = [int(item) for item in items]
            if numeric_items == list(range(len(numeric_items))):
                # Already 0, 1, 2, 3... format
                return {str(item): int(item) for item in items}
        except:
            pass

    # For multi-class target, create sequential mapping (0, 1, 2, 3...)
    if len(items) > 2:
        result = {}
        for i, item in enumerate(items):
            result[str(item)] = i
        return result

    # For binary classification target, use smart mapping
    positives = [
        'true',
        '1',
        'positive',
        'pos',
        'present',
        'yes',
        'active'
    ]

    result = {}

    for item in items:
        item_match = str(item).lower()
        val = any(list(map(lambda x: x in item_match, positives)))
        result[str(item)] = int(val)

    if (0 in result.values() and 1 in result.values()):
        return result

    else:
        pick = list(result.keys())[0]
        result[str(pick)] = int(not bool(result[str(pick)]))
        return result
