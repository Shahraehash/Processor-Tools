
import pandas as pd
import numpy as np

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params, global_params

#LOCAL HELPERS



def fill_in_zeros(dict):
    if not 1 in dict:
        dict[1] = 0
    if not 0 in dict:
        dict[0] = 0
    return dict

def counts_to_percent(df):
    return df['counts'] / df['counts'].sum() * 100


def merged_files_describe(df,target):

    describe = {}

    #counts
    total_df = pd.DataFrame(df[target].value_counts())
    total_df.rename(columns={target: 'counts'}, inplace=True)
    #percentage
    total_df['percent'] = counts_to_percent(total_df)

    total_df.loc['total'] = total_df.sum() #make total row

    describe['total'] = total_df.to_dict()        


    #nan values
    nan_df = df[df.isna().any(axis=1)][target].value_counts()
    nan_df = fill_in_zeros(nan_df)

    nan_df = pd.DataFrame(nan_df)
    nan_df.rename(columns={target: 'counts'}, inplace=True)

    nan_df['percent'] = round(nan_df['counts'] / total_df['counts'].loc['total'] * 100,1)

    nan_df.loc['total'] = nan_df.sum() #make total row

    describe['nan'] = nan_df.to_dict()


    #normal values
    non_nan_df = df[~df.isna().any(axis=1)][target].value_counts()
    non_nan_df = fill_in_zeros(non_nan_df)

    non_nan_df = pd.DataFrame(non_nan_df)
    non_nan_df.rename(columns={target: 'counts'}, inplace=True)

    non_nan_df['percent'] = counts_to_percent(non_nan_df)

    non_nan_df['percent'] = round(non_nan_df['counts'] / total_df['counts'].loc['total'] * 100,1)

    non_nan_df.loc['total'] = non_nan_df.sum() #make total row

    describe['non_nan'] = non_nan_df.to_dict()
    

    major = df[target].value_counts().idxmax()
    minor = df[target].value_counts().idxmin()

    #if the class sizes are the same, check to see if the non_missing data classes are the same and base the assignement on that
    if major == minor:
        if describe['non_nan']['counts'][0] > describe['non_nan']['counts'][1]:
            major = 0
            minor = 1
        else:
            major = 1
            minor = 0


    describe['major'] = int(major)
    describe['minor'] = int(minor)

    return describe



def merge_files_training_class_size(describe_obj):
    #takes describe object from merged_files_describe() and returns the appropriate class size for training
    minor_class = describe_obj['minor']
    minor_class_non_nan_counts = describe_obj["non_nan"]['counts'][minor_class]

    half_minor_class_non_nan_counts = round(minor_class_non_nan_counts / 2)


    min_training_class_size = global_params()['min_training_class_size']

    if half_minor_class_non_nan_counts < min_training_class_size:
        return min_training_class_size
    else:
        return half_minor_class_non_nan_counts



#this function is legacy and will be removed
def merge_files_segments(describe_obj, training_class_size, missing_values_option, prevelence_option):

    print(describe_obj)

    major = describe_obj['major']
    minor = describe_obj['minor']


    #special condition to convert keys that are normally ints to strings if passed via json to avoid key error later
    #this applies only when applying the effect function because the describe_obj is coming from the front end
    try:
        describe_obj['non_nan']['counts'][major]
    except:
        major = str(describe_obj['major'])
        minor = str(describe_obj['minor'])


    if missing_values_option == 0 and prevelence_option == 0:
        #remove all rows with missing values and use all data
        test_major = describe_obj['non_nan']['counts'][major] - training_class_size
        test_minor = describe_obj['non_nan']['counts'][minor] - training_class_size
        remainder = describe_obj['nan']['counts'][major] + describe_obj['nan']['counts'][minor]
    
    elif missing_values_option == 0 and prevelence_option == 1:
        #remove all rows with missing values and keep original prevalences

        test_minor = describe_obj['non_nan']['counts'][minor] - training_class_size  

        ##TODO: make sure the right prevalences are used
        minor_prev = (describe_obj['total']['percent'][minor] / 100)
        major_prev = (describe_obj['total']['percent'][major] / 100)

        test_major = round((test_minor / minor_prev) * major_prev)
        print(test_major)
        remainder = describe_obj['nan']['counts'][minor] + describe_obj['nan']['counts'][major]  + (describe_obj['non_nan']['counts'][major] - test_major - training_class_size) 

    elif missing_values_option == 1 and prevelence_option == 0:
        test_major = describe_obj['total']['counts'][major] - training_class_size
        test_minor = describe_obj['total']['counts'][minor] - training_class_size
        remainder = 0     

    elif missing_values_option == 1 and prevelence_option == 1:
        test_minor = describe_obj['total']['counts'][minor] - training_class_size

        minor_prev = (describe_obj['total']['percent'][minor] / 100)
        major_prev = (describe_obj['total']['percent'][major] / 100)

        test_major = round((test_minor / minor_prev) * major_prev)

        remainder = describe_obj['total']['counts'][major] - training_class_size - test_major             


    total = describe_obj['total']['counts'][major] + describe_obj['total']['counts'][minor]


    return {
        'train': {
            'counts': {
                major: training_class_size,
                minor: training_class_size
            },
            'percent': {
                major: round((training_class_size / total) * 100,1) - 1,
                minor: round((training_class_size / total) * 100,1) - 1
            }
        },
        'test': {
            'counts': {
                major: test_major,
                minor: test_minor
            },
            'percent': {
                major: round((test_major / total) * 100,1) - 1,
                minor: round((test_minor / total) * 100,1) -1 
            }            
        },
        'remainder': {
            'counts': remainder,
            'percent': round((remainder / total) * 100,1)
        },
        'missing_values_option': missing_values_option,
        'prevelence_option': prevelence_option,
        'major': major,
        'minor': minor
    }





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

            describe_obj = merged_files_describe(df,target)

            groups_result[group] = {}
            groups_result[group]['describe'] =  describe_obj
            training_class_size = merge_files_training_class_size(describe_obj)
            groups_result[group]['training_class_size'] = training_class_size
            groups_result[group]['segments'] = merge_files_segments(describe_obj, training_class_size, 0, 1) #we don't actually use this now TODO

           

    return {'fileAnalysisDict': groups_result} 


#EFFECT
def effect_train_test_split_impute(fileObjectArray, target, effect):

    segments = merge_files_segments(
        effect['describeObj'],
        effect['trainingClassSize'], 
        effect['missingValuesOption'], 
        effect['prevalenceOption']
        )

    return segments
    
    
    
    
    
    #return merge_files_segments(describe_obj, training_class_size, missing_values_options, prevelence_option)


#TRANSFORM
def transform_train_test_split_impute(fileObjectArray, target, transform):

    ##OUTPUT FILE NAMES
    train_file_name = 'training_and_initial_validation.csv'
    test_file_name = 'generalization_testing.csv'
    removed__file_name = 'removed_values.csv'
    imputed_file_name = 'imputed_values.csv'


    groups = {
        'train': [],
        'test': [],
        'combined': [],
        'unknown': []
    }

    df_groups = {}

    
    result_array = []
    for file in fileObjectArray:

        print()

        df = load_file(file['storageId'])   

        #track original index
        df['origin_file_name'] = file['name']
        df['origin_file_source_row'] = df.index

        if file['type'] == None:
            groups['unknown'].append(df)
        else:
            groups[file['type']].append(df)
        
    for group in groups:
        if len(groups[group]) > 0:
            df = pd.concat(groups[group])

            df_groups[group] = df
    
    


    
    result = []


    #multiple files

    if 'train' in df_groups and 'test' in df_groups:
        
        t = transform['data']
        training_missing_setting = t['trainMissing'] #drop missing = 0, impute = 1
        training_equalizate_setting = t['trainEqualize'] #no change = 0, equalize = 1
        testing_missing = t['testMissing'] #drop missing = 0, only option currently
        testing_prevalence = t['testPrevalence'] #use all data = 0, adjust to origial = 1

        #define DFs
        df_train = df_groups['train']
        df_test = df_groups['test']

        #Training
        array_df_removed = []

        #if drop missing rows
        if training_missing_setting == 0:
            df_train_nan = df_train[df_train.isna().any(axis=1)]
            df_train = df_train.drop(df_train_nan.index)
            array_df_removed.append(df_train_nan)

        #if impute missing rows
        elif training_missing_setting == 1:
            df_train, df_imputed = impute_processor(df_train, target)

        #if equalize classes
        if training_equalizate_setting == 1:
            df_train[target].value_counts().to_dict()
            value_counts = df_train[target].value_counts().to_dict()
            goal = df_train[target].value_counts().min()
            for key in value_counts:
                temp_drop = df_train[df_train[target] == key].sample(value_counts[key] - goal, replace=False)
                print(temp_drop.shape)
                df_train.drop(temp_drop.index, inplace=True)
                array_df_removed.append(temp_drop)

        #TESTING
        #must drop missing rows
        df_test_nan = df_test[df_test.isna().any(axis=1)]
        df_test = df_test.drop(df_test_nan.index)
        array_df_removed.append(df_test_nan)

        #use all data or adjust prevlence to match original dataset
        if testing_prevalence == 0:
            pass
        elif testing_prevalence == 1:
            df_test[target].value_counts().to_dict()
            value_counts = df_test[target].value_counts().to_dict()
            for key in value_counts:
                goal = t['finalValues']['total']['test'][str(key)]
                temp_drop = df_test[df_test[target] == key].sample(value_counts[key] - goal, replace=False)
                print(temp_drop.shape)
                df_test.drop(temp_drop.index, inplace=True)
                array_df_removed.append(temp_drop)
        
        df_removed = pd.concat(array_df_removed)

        #file names defined at top of method
        #include dropped output in result
        if df_removed.shape[0] > 0:
            result.append(store_file_and_params(df_removed, removed__file_name, 'removed'))

        result.append(store_file_and_params(df_train, train_file_name, 'train'))
        result.append(store_file_and_params(df_test, test_file_name, 'test'))


    elif 'combined' in df_groups:

        t = transform['data']
        print(t)


        missing_value_setting = t['missingValuesOption'] #drop missing = 0, impute = 1
        testing_prevalence = t['prevalenceOption'] #use all data = 0, adjust to origial = 1
        training_class_size = t['trainingClassSize']

        df = df_groups['combined']

        array_df_removed = []

        df_class_zero = df[df[target] == 0]
        df_class_one = df[df[target] == 1]

        df_nan_class_zero = df_class_zero[df_class_zero.isna().any(axis=1)]
        df_nan_class_one = df_class_one[df_class_one.isna().any(axis=1)]


        print(df_class_zero.shape)
        print(df_class_one.shape)
        print(df_nan_class_zero.shape)
        print(df_nan_class_one.shape)

        print(df_nan_class_one.head(1))

        
        #if drop missing value rows
       
        if missing_value_setting == 0:
            #remove missing values
            df_class_zero = df_class_zero.drop(df_nan_class_zero.index)
            df_class_one = df_class_one.drop(df_nan_class_one.index)

            #track missing values
            array_df_removed.append(df_nan_class_zero)
            array_df_removed.append(df_nan_class_one)

            #sample training data
            df_training_zero = df_class_zero.sample(training_class_size, replace=False)
            df_training_one = df_class_one.sample(training_class_size, replace=False)

            #combine training data
            df_train = pd.concat([df_training_zero, df_training_one])

            #remove training data from original sample
            df_class_zero.drop(df_training_zero.index, inplace=True)
            df_class_one.drop(df_training_one.index, inplace=True)

        #if impute missing value rows
         #TODO handle case if missing values > training class size
        elif missing_value_setting == 1:
            #isolate missing values
            df_class_zero = df_class_zero.drop(df_nan_class_zero.index)
            df_class_one = df_class_one.drop(df_nan_class_one.index)

            #sample training data minus missing values
            df_training_zero = df_class_zero.sample(training_class_size - df_nan_class_zero.shape[0], replace=False)
            df_training_one = df_class_one.sample(training_class_size - df_nan_class_one.shape[0], replace=False)

            #remove training data from original sample
            df_class_zero.drop(df_training_zero.index, inplace=True)
            df_class_one.drop(df_training_one.index, inplace=True)

            df_train = pd.concat([df_training_zero, df_nan_class_zero, df_training_one, df_nan_class_one])


            df_train, df_imputed = impute_processor(df_train, target)


        #testing prevalance already set in front end, no further math needed based on settings
        test_counts = t['finalValues']['total']['test']

        #sample testing data
        #must use string as key since passed as JSON
        df_testing_zero = df_class_zero.sample(test_counts['0'], replace=False)
        df_testing_one = df_class_one.sample(test_counts['1'], replace=False)

        #remove testing data from pool
        df_class_zero.drop(df_testing_zero.index, inplace=True)
        df_class_one.drop(df_testing_one.index, inplace=True)

        #put remaining data in removed
        array_df_removed.append(df_class_zero)
        array_df_removed.append(df_class_one)

        #combine testing data
        df_test = pd.concat([df_testing_zero, df_testing_one])


        #combined removed
        df_removed = pd.concat(array_df_removed)





        
        #file names defined at top of method
        result.append(store_file_and_params(df_train, train_file_name, 'train'))
        result.append(store_file_and_params(df_test, test_file_name, 'test'))

        if df_removed.shape[0] > 0:
            result.append(store_file_and_params(df_removed, removed__file_name, 'removed'))

        try:
            result.append(store_file_and_params(df_imputed, imputed_file_name, 'imputed'))
        except:
            pass
    

    return result




        
    
        

def impute_processor(df, target):


        imp_mean = IterativeImputer(random_state=0)
        X = df.drop(columns=[target])
        y = df[target]

        imputed_row_index = list(df[df.isna().any(axis=1)].index)

        print(imputed_row_index)
        extra = df[['origin_file_name', 'origin_file_source_row']]
        X = X.drop(columns=['origin_file_name', 'origin_file_source_row'])

        #check if negative values exist in each column before imputation
        col_has_negative = ((X < 0).any()).to_dict()


        #flag columns for rounding
        col_is_binary = []
        col_is_numeric_cat = {}

        for col in X.columns:
            feature = X[col]
            
            if feature.isna().sum() > 0: #ensure has nan values
                unique = feature.dropna().unique()
                unique.sort()
                unique_int_len = len(list(filter(lambda x: x.is_integer(), unique))) #checks to ensure values are ints even if cast as float                    

                if len(unique) == unique_int_len and (unique_int_len <= 20): #set 
                    col_is_numeric_cat[col] = unique


        imp_mean.fit(X)
        result = pd.DataFrame(imp_mean.transform(X),columns=X.columns, index=X.index)
        result[df.columns[df.isna().any()]] = result[df.columns[df.isna().any()]].round(decimals=3)

        #if column does not have negative values, change all imputed negative values to 0
        for col in col_has_negative:
            if(not col_has_negative[col]):
                column = result[col]
                column[column < 0 ] = 0
        
        # #round one hot encoded columns

        ###TODO fix this
        # for col in columns_added:
        #     result[col] = result[col].round()

        # ensure numerical categorial data is maintained with imputation
        for col in col_is_numeric_cat.keys():
            result[col] = result[col].round().astype(int)
            possible_values = col_is_numeric_cat[col]
            
            #find values not matching original values in data set
            extra_value_bool = ~result[col].isin(possible_values)
            extra_values = result[col][extra_value_bool].unique()
            
            #find the closest original value and adjust it
            for val in extra_values:
                arr = np.asarray(possible_values)
                i = (np.abs(arr - val)).argmin()
                closest = arr[i]
                result[col] = result[col].replace(val, closest)



        result[target] = y
        result['origin_file_name'] = extra['origin_file_name']
        result['origin_file_source_row'] = extra['origin_file_source_row']

        imputed = result.loc[imputed_row_index]
        #becaause of how the indexes are tracked, it becomes cast as a string and needs loc rather than iloc

        return result, imputed









