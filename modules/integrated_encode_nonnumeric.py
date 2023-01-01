
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params, create_binary_map


#ANALYSIS

def analyze_encode_nonnumeric(fileObjectArray, target):
    df_array = []
    for file in fileObjectArray:

        df = load_file(file['storageId'])   
        df_array.append(df)

    df = pd.concat(df_array)

    print(df.shape)


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
                'values' : {
                    'counts': int(numeric_count),
                    'percent': float(round(numeric_count / total_count * 100))
                },
                'items': [
                    {'text': 'Convert column to numeric', 'value': 'mixed_to_numeric'},
                    {'text': 'Remove column', 'value': 'drop'}
                ],
                'selection': 'mixed_to_numeric'
            }
            result.append(t)

        else:
            list_length = len(list(col.unique()))

            print()
            if list_length == 1:


                t = {
                    'name': column,
                    'method': 'drop_single',
                    'unique_values': list(col.unique()),
                    'nan_row_index': list(col[col.isna() == True].index),
                    'items': [
                        {'text': 'Remove column', 'value': 'drop'},
                    ],
                    'selection': 'drop'
                }       

            elif list_length == 2:


                #give option to map values
                value_map = create_binary_map(list(col.unique()))
    
                t = {
                    'name': column,
                    'method': 'one_hot_encode_binary',
                    'unique_values': list(col.unique()),
                    'nan_row_index': list(col[col.isna() == True].index),
                    'items': [
                        {'text': 'Convert each unique value to a seperate binary column', 'value': 'one_hot_encode'},
                        {'text': 'Encode as a single binary column', 'value': 'binary_encode'},
                        {'text': 'Remove column', 'value': 'drop'}
                    ],
                    'selection': 'one_hot_encode',
                    'valueMap': value_map
                }     

            else:    



                t = {
                    'name': column,
                    'method': 'one_hot_encode',
                    'unique_values': list(col.unique()),
                    'nan_row_index': list(col[col.isna() == True].index),
                    'items': [
                        {'text': 'Convert each unique value to a seperate binary column', 'value': 'one_hot_encode'},
                        {'text': 'Remove column', 'value': 'drop'},
                    ],
                    'selection': 'one_hot_encode' if len(list(col.unique())) <=20 else 'drop' #rule to decide if column should be dropped by default
                }
            #ADD LATER
            # if len(t['unique_values']) == 2: #allow for boolean conversion if only two unique values
            #     t['items'].insert(1,{'text': 'Convert to boolean', 'value': 'mixed_to_boolean'}) 
            #     if True in t['unique_values']: #if true is one of the unique values, then use this as default
            #         t['selection'] = 'mixed_to_boolean'

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

    df = pd.concat(df_array) #combine all files into one dataframe

    

    

    for column in transform['data']:




        if column['selection'] == 'mixed_to_numeric':
            print(column['name'])
            df[column['name']] = local_transform_mixed_to_numeric(df[column['name']])

        #ADD LATER
        # elif t['type'] == 'category_to_binary':
        #     df[column] = transform_category_to_binary(df[column], t['map'])
        
        elif column['selection'] == 'one_hot_encode':
            df = pd.concat([df, local_transform_one_hot_encode(df[column['name']])], axis=1)
            df = df.drop(column['name'], axis=1)

        elif column['selection'] == 'drop':
            df = df.drop(column['name'], axis=1)

        elif column['selection'] == 'binary_encode':
             #the valueMap property is created on the backend when two unique values exist and maniplated on front end
            df[column['name']] = df[column['name']].astype('str').map(column['valueMap']).astype('int')

        #ensure target remains at end of file


    col_list = list(df.columns)
    i = col_list.index(target)
    reorder_list = col_list[:i] + col_list[i + 1:] + [target]
    df = df[reorder_list]

    
    
    #Split files and save

    print(df.columns)
    result = []

    grouped = df.groupby(df.storage_id)
    for file in fileObjectArray:
        file_index=0
        df = grouped.get_group(file['storageId'])
        df = df.drop('storage_id', axis=1)

        result.append(store_file_and_params(df, file['name'], file['type']))
        file_index += 1
    
    return result





def local_transform_mixed_to_numeric(series):
    """
    Convert a series of mixed data types to numeric
    input: series
    """

    # non-numerics are converted to NaN and removed
    output = pd.to_numeric(series, errors='coerce')
    #output = output.dropna()        

    return output

def local_transform_one_hot_encode(series):
    working = pd.Series(series)
    working = working.dropna()
    index = working.index
    
    enc = OneHotEncoder(handle_unknown='ignore')
    vector = working.values.reshape(-1,1)
    enc.fit(vector)
    trans = enc.transform(vector).toarray()
    output = pd.DataFrame(trans, columns=enc.categories_, index=index).add_prefix(series.name + '_').astype('int')
    output.columns = output.columns.get_level_values(0) #convert multiindex to single index
    
    return output

#ADD LATER
# def transform_category_to_binary(series, map):
#     return series.map(map).astype('int')