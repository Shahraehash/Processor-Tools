
import pandas as pd
import numpy as np

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params

#LOCAL HELPERS
def fill_in_zeros(dict):
    if not 1 in dict:
        dict[1] = 0
    if not 0 in dict:
        dict[0] = 0
    return dict

def counts_to_percent(df):
    return round(df['counts'] / df['counts'].sum() * 100,1)


def analyze_merged_files(df,target, training_size):

    describe = {}

    #counts
    total_df = pd.DataFrame(df[target].value_counts())
    total_df.rename(columns={target: 'counts'}, inplace=True)
    #percentage
    total_df['percent'] = counts_to_percent(total_df)

    describe['total'] = total_df.to_dict()        

    nan_df = df[df.isna().any(axis=1)][target].value_counts()
    nan_df = fill_in_zeros(nan_df)

    nan_df = pd.DataFrame(nan_df)
    nan_df.rename(columns={target: 'counts'}, inplace=True)

    nan_df['percent'] = round(nan_df['counts'] / total_df['counts'].sum() * 100,1)


    describe['nan'] = nan_df.to_dict()


    non_nan_df = df[~df.isna().any(axis=1)][target].value_counts()
    non_nan_df = fill_in_zeros(non_nan_df)

    non_nan_df = pd.DataFrame(non_nan_df)
    non_nan_df.rename(columns={target: 'counts'}, inplace=True)

    non_nan_df['percent'] = counts_to_percent(non_nan_df)

    non_nan_df['percent'] = round(non_nan_df['counts'] / total_df['counts'].sum() * 100,1)

    describe['non_nan'] = non_nan_df.to_dict()
    

    major = df[target].value_counts().idxmax()
    minor = df[target].value_counts().idxmin()

    test_major = total_df['counts'][major] - training_size
    test_minor = total_df['counts'][minor] - training_size

    total = test_major + test_minor + (2 * training_size)

    classes = {
        'train': {
            'total': {
                'counts': int(training_size * 2),
                'percent': float(round(training_size * 2 / total * 100, 1))
            },
            'counts' : {
                major: int(training_size),
                minor: int(training_size)
            },
            'percent': {
                major: float(round(training_size / total * 100, 1)),
                minor: float(round(training_size / total * 100, 1)),
            }
        },
        'test': {
            'total':  {
                'counts': int(test_major + test_minor),
                'percent': float(round((test_major + test_minor) / total * 100, 1))
            },
            'counts' : {
                major: int(test_major),
                minor: int(test_minor)
            },
            'percent': {
                major: float(round(test_major / total * 100, 1)),
                minor: float(round(test_minor / total * 100, 1)),
            }

        }
    }    


    result = {
        'class': {
            'major': int(major),
            'minor': int(minor)
        },
        'describe': describe,
        'classes': classes
    }  
    return result   


#ANALYSIS

def analyze_train_test_split_impute(fileObjectArray, target):
    groups = {
        'train': [],
        'test': [],
        'combined': [],
        'unknown': []
    }

    groups_result = {}

    
    result_array = []
    for file in fileObjectArray:

        print()

        df = load_file(file['storageId'])   
        if file['type'] == None:
            groups['unknown'].append(df)
        else:
            groups[file['type']].append(df)
        
    for group in groups:
        if len(groups[group]) > 0:
            df = pd.concat(groups[group])
            groups_result[group] = analyze_merged_files(df,target, 25)

    return {'fileAnalysisDict': groups_result} 


#EFFECT
#none


#TRANSFORM
