
import pandas as pd
import numpy as np

from .helpers import load_file, save_file, file_params, int_list_to_string


#ANALYSIS

def analysis_encode_nonnumeric(fileObjectArray, target):
    df_array = []
    for file in fileObjectArray:

        df = load_file(file['storageId'])   
        df_array.append(df)

    df = pd.concat(df_array)


    valid_data_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'bool']

    valid = df.select_dtypes(include=valid_data_types)

    invalid = df.drop(columns=valid.columns)

    result = []

    for column in invalid.columns:
        col = invalid[column]

        total_count = col.shape[0]
        nan_count = col.isna().sum()

        col = col.dropna()
        not_nan_count = col.shape[0]

        numeric = ~pd.to_numeric(col, errors='coerce').isna()
        numeric_count = numeric.sum()

        if (numeric_count / total_count) > 0.6:
            invalid[column] = pd.to_numeric(col, errors='coerce')
            #proposed_transform
            t = {
                'name': column,
                'method': 'mixed_to_numeric',
                'nan_row_index': list(col[col.isna() == True].index),
                'non_numeric_row_index': list(numeric[numeric == False].index),
                'items': [
                    {'text': 'Convert to numeric', 'value': 'mixed_to_numeric'},
                    {'text': 'Remove column', 'value': 'drop'}
                ],
                'selection': 'mixed_to_numeric'
            }
            result.append(t)

        else:
            t = {
                'name': column,
                'method': 'one_hot_encode',
                'unique_values': list(col.unique()),
                'nan_row_index': list(col[col.isna() == True].index),
                'items': [
                    {'text': 'Covert each unique value to a column', 'value': 'one_hot_encode'},
                    {'text': 'Remove column', 'value': 'drop'},
                ],
                'selection': 'one_hot_encode' if len(list(col.unique())) <=20 else 'drop' #rule to decide if column should be dropped by default
            }
            if len(t['unique_values']) == 2: #allow for boolean conversion if only two unique values
                t['items'].insert(1,{'text': 'Convert to boolean', 'value': 'mixed_to_boolean'}) 
                if True in t['unique_values']: #if true is one of the unique values, then use this as default
                    t['selection'] = 'mixed_to_boolean'

            result.append(t)
    return {'fileAnalysisCombined': result} 


#EFFECT
#none


#TRANSFORM
def transform_encode_nonnumeric(fileObjectArray, target, transform):
    df_array = []
    for file in fileObjectArray:

        df_sub = load_file(file['storageId'])
        df_sub['storage_id'] = file['storageId']
        df_array.append(df_sub)

    df = pd.concat(df_array)
    id = df['storage_id']
    df = df.drop(columns=['storage_id'])



    for t in transform.data:
        print(t['selection'])




    #     if t['type'] == 'mixed_to_numeric':
    #         df[column] = transform_mixed_to_numeric(df[column])

    #     elif t['type'] == 'category_to_binary':
    #         df[column] = transform_category_to_binary(df[column], t['map'])
        
    #     elif t['type'] == 'one_hot_encode':
    #         #if meets rules or user elects to keep
    #         if t['keep_column']:
    #             df = pd.concat([df, transform_one_hot_encode(df[column])], axis=1)
    #         df = df.drop(column, axis=1)

    # try:
    #     df[target] = df[target].astype('str').map(target_map).astype('int')
    # except:
    #     print('ERROR APPLYING TARGET MAP')

    # #ensure target remains at end of file
    # col_list = list(df.columns)
    # i = col_list.index(target)
    # reorder_list = col_list[:i] + col_list[i + 1:] + [target]
    # df = df[reorder_list]
    # return df 


