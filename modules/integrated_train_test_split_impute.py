
import pandas as pd
import numpy as np

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params, global_params

#LOCAL HELPERS

def sort_values_original_order(df):
    if df.empty:
        print("WARNING: Attempting to sort empty DataFrame")
        return df
    
    # Check if required columns exist
    required_cols = ['origin_file_name', 'origin_file_source_row']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"WARNING: Missing columns for sorting: {missing_cols}")
        return df
    
    return df.sort_values(by=['origin_file_name','origin_file_source_row'])

def fill_in_zeros(dict):
    if not 1 in dict:
        dict[1] = 0
    if not 0 in dict:
        dict[0] = 0
    return dict

def counts_to_percent(df):
    total = df['counts'].sum()
    if total > 0:
        return round(df['counts'] / total * 100, 1)
    else:
        return pd.Series([0] * len(df), index=df.index)


def merged_files_describe(df,target):
    print(f"DEBUG: merged_files_describe called with df shape: {df.shape}, target: {target}")

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataframe")

    if df.empty:
        raise ValueError("DataFrame is empty")

    describe = {}
    
    # Get all unique classes in the target column
    unique_classes = sorted(df[target].dropna().unique())
    print(f"DEBUG: unique_classes: {unique_classes}")
    
    if len(unique_classes) == 0:
        raise ValueError(f"No valid values found in target column '{target}'")

    #counts
    total_counts = df[target].value_counts()
    total_df = pd.DataFrame({'counts': total_counts})
    total_df['percent'] = counts_to_percent(total_df)
    total_df.loc['total'] = total_df.sum() #make total row
    describe['total'] = total_df.to_dict()
    print(f"DEBUG: total counts: {describe['total']}")

    #nan values
    nan_rows = df[df.isna().any(axis=1)]
    if not nan_rows.empty:
        nan_counts = nan_rows[target].value_counts()
    else:
        nan_counts = pd.Series(dtype='int64')
    
    # Ensure all classes are represented - create a proper Series with all classes
    nan_counts_dict = {}
    for cls in unique_classes:
        nan_counts_dict[cls] = nan_counts.get(cls, 0)
    
    nan_counts = pd.Series(nan_counts_dict)
    nan_df = pd.DataFrame({'counts': nan_counts})
    
    # Safe division to avoid division by zero
    total_count = total_df['counts'].loc['total']
    if total_count > 0:
        nan_df['percent'] = round(nan_df['counts'] / total_count * 100, 1)
    else:
        nan_df['percent'] = 0

    nan_df.loc['total'] = nan_df.sum() #make total row
    describe['nan'] = nan_df.to_dict()
    print(f"DEBUG: nan counts: {describe['nan']}")

    #normal values
    non_nan_rows = df[~df.isna().any(axis=1)]
    if not non_nan_rows.empty:
        non_nan_counts = non_nan_rows[target].value_counts()
    else:
        non_nan_counts = pd.Series(dtype='int64')
    
    # Fill in zeros for all classes that might not have non-NaN values - create a proper Series with all classes
    non_nan_counts_dict = {}
    for cls in unique_classes:
        non_nan_counts_dict[cls] = non_nan_counts.get(cls, 0)
    
    non_nan_counts = pd.Series(non_nan_counts_dict)
    non_nan_df = pd.DataFrame({'counts': non_nan_counts})
    
    # Safe division to avoid division by zero
    if total_count > 0:
        non_nan_df['percent'] = round(non_nan_df['counts'] / total_count * 100, 1)
    else:
        non_nan_df['percent'] = 0

    non_nan_df.loc['total'] = non_nan_df.sum() #make total row
    describe['non_nan'] = non_nan_df.to_dict()
    print(f"DEBUG: non_nan counts: {describe['non_nan']}")

    # For multi-class, identify majority and minority classes
    class_counts = df[target].value_counts()
    major = class_counts.idxmax()
    minor = class_counts.idxmin()

    # Store all unique classes for multi-class support (convert to regular Python types for JSON serialization)
    describe['unique_classes'] = [int(cls) if isinstance(cls, (int, np.integer)) else cls for cls in unique_classes]
    describe['num_classes'] = len(unique_classes)
    describe['major'] = int(major) if isinstance(major, (int, np.integer)) else major
    describe['minor'] = int(minor) if isinstance(minor, (int, np.integer)) else minor

    return describe



# def merge_files_training_class_size(describe_obj):
#     #takes describe object from merged_files_describe() and returns the appropriate class size for training
#     minor_class = describe_obj['minor']
#     minor_class_non_nan_counts = describe_obj["non_nan"]['counts'][minor_class]

#     half_minor_class_non_nan_counts = round(minor_class_non_nan_counts / 2)


#     min_training_class_size = global_params()['min_training_class_size']

#     if half_minor_class_non_nan_counts < min_training_class_size:
#         return min_training_class_size
#     else:
#         return half_minor_class_non_nan_counts



#this function is legacy and will be removed
def merge_files_segments(describe_obj, training_class_size, missing_values_option, prevelence_option):
    print(f"DEBUG: merge_files_segments called with training_class_size: {training_class_size}")
    print(f"DEBUG: describe_obj keys: {describe_obj.keys()}")
    print(f"DEBUG: unique_classes: {describe_obj.get('unique_classes', 'not found')}")
    print(f"DEBUG: num_classes: {describe_obj.get('num_classes', 'not found')}")

    # Handle multi-class scenarios
    if describe_obj.get('num_classes', 2) > 2:
        print("DEBUG: Multi-class scenario detected, returning simplified segments")
        # For multi-class, return a simplified structure
        unique_classes = describe_obj.get('unique_classes', [])
        total_samples = describe_obj['total']['counts'].get('total', 0)
        
        # Create a simplified response for multi-class
        train_counts = {}
        test_counts = {}
        
        for cls in unique_classes:
            cls_key = str(cls)
            total_cls_count = describe_obj['total']['counts'].get(cls, 0)
            train_counts[cls_key] = min(training_class_size, total_cls_count)
            test_counts[cls_key] = max(0, total_cls_count - train_counts[cls_key])
        
        total_train = sum(train_counts.values())
        total_test = sum(test_counts.values())
        remainder = max(0, total_samples - total_train - total_test)
        
        return {
            'train': {
                'counts': train_counts,
                'percent': {cls: round((count / total_samples) * 100, 1) if total_samples > 0 else 0 
                           for cls, count in train_counts.items()}
            },
            'test': {
                'counts': test_counts,
                'percent': {cls: round((count / total_samples) * 100, 1) if total_samples > 0 else 0 
                           for cls, count in test_counts.items()}
            },
            'remainder': {
                'counts': remainder,
                'percent': round((remainder / total_samples) * 100, 1) if total_samples > 0 else 0
            },
            'missing_values_option': missing_values_option,
            'prevelence_option': prevelence_option,
            'major': describe_obj.get('major', unique_classes[0] if unique_classes else 0),
            'minor': describe_obj.get('minor', unique_classes[-1] if unique_classes else 0)
        }

    # Original binary classification logic
    major = describe_obj['major']
    minor = describe_obj['minor']

    #special condition to convert keys that are normally ints to strings if passed via json to avoid key error later
    #this applies only when applying the effect function because the describe_obj is coming from the front end
    try:
        describe_obj['non_nan']['counts'][major]
    except:
        major = str(describe_obj['major'])
        minor = str(describe_obj['minor'])

    print(f"DEBUG: Binary classification - major: {major}, minor: {minor}")

    # Safe access to counts with error handling
    try:
        major_non_nan = describe_obj['non_nan']['counts'].get(major, 0)
        minor_non_nan = describe_obj['non_nan']['counts'].get(minor, 0)
        major_nan = describe_obj['nan']['counts'].get(major, 0)
        minor_nan = describe_obj['nan']['counts'].get(minor, 0)
        major_total = describe_obj['total']['counts'].get(major, 0)
        minor_total = describe_obj['total']['counts'].get(minor, 0)
        
        print(f"DEBUG: major_non_nan: {major_non_nan}, minor_non_nan: {minor_non_nan}")
        print(f"DEBUG: major_total: {major_total}, minor_total: {minor_total}")
        
    except Exception as e:
        print(f"ERROR accessing counts in merge_files_segments: {e}")
        # Return a safe default structure
        return {
            'train': {'counts': {major: 0, minor: 0}, 'percent': {major: 0, minor: 0}},
            'test': {'counts': {major: 0, minor: 0}, 'percent': {major: 0, minor: 0}},
            'remainder': {'counts': 0, 'percent': 0},
            'missing_values_option': missing_values_option,
            'prevelence_option': prevelence_option,
            'major': major,
            'minor': minor
        }

    if missing_values_option == 0 and prevelence_option == 0:
        #remove all rows with missing values and use all data
        test_major = max(0, major_non_nan - training_class_size)
        test_minor = max(0, minor_non_nan - training_class_size)
        remainder = major_nan + minor_nan
    
    elif missing_values_option == 0 and prevelence_option == 1:
        #remove all rows with missing values and keep original prevalences
        test_minor = max(0, minor_non_nan - training_class_size)

        ##TODO: make sure the right prevalences are used
        minor_prev = (describe_obj['total']['percent'].get(minor, 0) / 100)
        major_prev = (describe_obj['total']['percent'].get(major, 0) / 100)

        if minor_prev > 0:
            test_major = round((test_minor / minor_prev) * major_prev)
        else:
            test_major = 0
        remainder = major_nan + minor_nan + max(0, major_non_nan - test_major - training_class_size)

    elif missing_values_option == 1 and prevelence_option == 0:
        test_major = max(0, major_total - training_class_size)
        test_minor = max(0, minor_total - training_class_size)
        remainder = 0     

    elif missing_values_option == 1 and prevelence_option == 1:
        test_minor = max(0, minor_total - training_class_size)

        minor_prev = (describe_obj['total']['percent'].get(minor, 0) / 100)
        major_prev = (describe_obj['total']['percent'].get(major, 0) / 100)

        if minor_prev > 0:
            test_major = round((test_minor / minor_prev) * major_prev)
        else:
            test_major = 0

        remainder = max(0, major_total - training_class_size - test_major)

    total = major_total + minor_total

    return {
        'train': {
            'counts': {
                major: training_class_size,
                minor: training_class_size
            },
            'percent': {
                major: round((training_class_size / total) * 100,1) if total > 0 else 0,
                minor: round((training_class_size / total) * 100,1) if total > 0 else 0
            }
        },
        'test': {
            'counts': {
                major: test_major,
                minor: test_minor
            },
            'percent': {
                major: round((test_major / total) * 100,1) if total > 0 else 0,
                minor: round((test_minor / total) * 100,1) if total > 0 else 0
            }            
        },
        'remainder': {
            'counts': remainder,
            'percent': round((remainder / total) * 100,1) if total > 0 else 0
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

        df = load_file(file['storageId'])
        if file['type'] == None:
            groups['unknown'].append(df)
        else:
            groups[file['type']].append(df)
        
    for group in groups:
        if len(groups[group]) > 0:
            df = pd.concat(groups[group])
            print(f"DEBUG: Processing group '{group}' with df shape: {df.shape}")

            describe_obj = merged_files_describe(df,target)
            print(f"DEBUG: merged_files_describe completed for group '{group}'")

            groups_result[group] = {}
            groups_result[group]['describe'] =  describe_obj
            training_class_size = 25 #merge_files_training_class_size(describe_obj)
            groups_result[group]['training_class_size'] = training_class_size
            
            print(f"DEBUG: About to call merge_files_segments for group '{group}'")
            try:
                groups_result[group]['segments'] = merge_files_segments(describe_obj, training_class_size, 0, 1) #we don't actually use this now TODO
                print(f"DEBUG: merge_files_segments completed for group '{group}'")
            except Exception as e:
                print(f"ERROR in merge_files_segments for group '{group}': {e}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                raise

           

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
            if not df_train.empty:
                df_train[target].value_counts().to_dict()
                value_counts = df_train[target].value_counts().to_dict()
                goal = df_train[target].value_counts().min()
                for key in value_counts:
                    samples_to_drop = value_counts[key] - goal
                    if samples_to_drop > 0:
                        class_subset = df_train[df_train[target] == key]
                        if len(class_subset) >= samples_to_drop:
                            temp_drop = class_subset.sample(samples_to_drop, replace=False)
                            print(temp_drop.shape)
                            df_train.drop(temp_drop.index, inplace=True)
                            array_df_removed.append(temp_drop)
                        else:
                            print(f"WARNING: Not enough samples to drop for class {key}. Available: {len(class_subset)}, Required: {samples_to_drop}")

        #TESTING
        #must drop missing rows
        df_test_nan = df_test[df_test.isna().any(axis=1)]
        df_test = df_test.drop(df_test_nan.index)
        array_df_removed.append(df_test_nan)

        #use all data or adjust prevlence to match original dataset
        if testing_prevalence == 0:
            pass
        elif testing_prevalence == 1:
            if not df_test.empty:
                df_test[target].value_counts().to_dict()
                value_counts = df_test[target].value_counts().to_dict()
                for key in value_counts:
                    goal = t['finalValues']['total']['test'][str(key)]
                    samples_to_drop = value_counts[key] - goal
                    if samples_to_drop > 0:
                        class_subset = df_test[df_test[target] == key]
                        if len(class_subset) >= samples_to_drop:
                            temp_drop = class_subset.sample(samples_to_drop, replace=False)
                            print(temp_drop.shape)
                            df_test.drop(temp_drop.index, inplace=True)
                            array_df_removed.append(temp_drop)
                        else:
                            print(f"WARNING: Not enough test samples to drop for class {key}. Available: {len(class_subset)}, Required: {samples_to_drop}")
        
        # Safe concatenation to avoid axis=0 error with empty DataFrames
        non_empty_removed = [df for df in array_df_removed if not df.empty]
        df_removed = pd.concat(non_empty_removed) if non_empty_removed else pd.DataFrame()
        print(f"DEBUG: df_removed shape after concat: {df_removed.shape}")

        #file names defined at top of method
        #include dropped output in result
        if df_removed.shape[0] > 0:
            #sort
            df_removed = sort_values_original_order(df_removed)
            #output
            result.append(store_file_and_params(df_removed, removed__file_name, 'removed'))

        try:
            #sort
            df_imputed = sort_values_original_order(df_imputed)
            result.append(store_file_and_params(df_imputed, imputed_file_name, 'imputed'))
        except:
            pass

        #sort
        df_train = sort_values_original_order(df_train)
        df_test = sort_values_original_order(df_test)

        #output
        result.append(store_file_and_params(df_train, train_file_name, 'train'))
        result.append(store_file_and_params(df_test, test_file_name, 'test'))


    elif 'combined' in df_groups:

        t = transform['data']

        missing_value_setting = t['missingValuesOption'] #drop missing = 0, impute = 1
        testing_prevalence = t['prevalenceOption'] #use all data = 0, adjust to origial = 1
        training_class_size = t['trainingClassSize']

        df = df_groups['combined']

        array_df_removed = []

        # Get all unique classes dynamically
        unique_classes = sorted(df[target].dropna().unique())
        print(f"DEBUG: Processing {len(unique_classes)} classes: {unique_classes}")
        
        # Create dictionaries to hold class-specific dataframes
        df_classes = {}
        df_nan_classes = {}
        
        # Split data by class
        for cls in unique_classes:
            df_classes[cls] = df[df[target] == cls]
            df_nan_classes[cls] = df_classes[cls][df_classes[cls].isna().any(axis=1)]
            print(f"DEBUG: Class {cls} - Total: {len(df_classes[cls])}, NaN: {len(df_nan_classes[cls])}")
       
        
        #if drop missing value rows
       
        if missing_value_setting == 0:
            #remove missing values for all classes
            for cls in unique_classes:
                df_classes[cls] = df_classes[cls].drop(df_nan_classes[cls].index)
                #track missing values
                array_df_removed.append(df_nan_classes[cls])

            #sample training data for all classes
            train_arrays = []
            for cls in unique_classes:
                print(f"DEBUG: Class {cls} shape before sampling: {df_classes[cls].shape}")
                print(f"DEBUG: training_class_size: {training_class_size}")
                
                if len(df_classes[cls]) >= training_class_size:
                    df_training_class = df_classes[cls].sample(training_class_size, replace=False)
                    train_arrays.append(df_training_class)
                    #remove training data from original sample
                    df_classes[cls].drop(df_training_class.index, inplace=True)
                else:
                    print(f"WARNING: Not enough class {cls} samples. Available: {len(df_classes[cls])}, Required: {training_class_size}")
                    if len(df_classes[cls]) > 0:
                        train_arrays.append(df_classes[cls])
                        df_classes[cls] = df_classes[cls].iloc[0:0]  # Empty the dataframe

            #combine training data
            non_empty_train_arrays = [df for df in train_arrays if not df.empty]
            df_train = pd.concat(non_empty_train_arrays) if non_empty_train_arrays else pd.DataFrame()
            print(f"DEBUG: df_train shape after sampling: {df_train.shape}")

        #if impute missing value rows
        #TODO handle case if missing values > training class size
        elif missing_value_setting == 1:
            
            print(t)

            #remove missing values from non-nan data for all classes
            for cls in unique_classes:
                df_classes[cls] = df_classes[cls].drop(df_nan_classes[cls].index)
                print(f'class {cls}', df_classes[cls].shape)

            train_arrays = []

            # Process each class dynamically
            for cls in unique_classes:
                cls_str = str(cls)  # Convert to string for JSON key access
                
                # Get counts from frontend calculations
                train_imputed_count = t['finalValues']['imputed']['train'].get(cls_str, 0)
                train_total_count = t['finalValues']['total']['train'].get(cls_str, 0)
                train_nonimputed_count = train_total_count - train_imputed_count
                
                print(f"DEBUG: Class {cls} - Total: {train_total_count}, Imputed: {train_imputed_count}, Non-imputed: {train_nonimputed_count}")

                #sample training data minus missing values
                if train_nonimputed_count > 0 and len(df_classes[cls]) >= train_nonimputed_count:
                    df_training_class = df_classes[cls].sample(train_nonimputed_count, replace=False)
                    df_classes[cls].drop(df_training_class.index, inplace=True)
                    train_arrays.append(df_training_class)
                elif train_nonimputed_count > 0:
                    print(f"WARNING: Not enough class {cls} non-imputed samples. Available: {len(df_classes[cls])}, Required: {train_nonimputed_count}")
                    if len(df_classes[cls]) > 0:
                        train_arrays.append(df_classes[cls])
                        df_classes[cls] = df_classes[cls].iloc[0:0]  # Empty the dataframe
                
                # Sample imputed training data
                if train_imputed_count > 0 and len(df_nan_classes[cls]) >= train_imputed_count:
                    df_train_impute = df_nan_classes[cls].sample(train_imputed_count, replace=False)
                    df_nan_classes[cls].drop(df_train_impute.index, inplace=True)
                    train_arrays.append(df_train_impute)
                elif train_imputed_count > 0:
                    print(f"WARNING: Not enough class {cls} imputed samples. Available: {len(df_nan_classes[cls])}, Required: {train_imputed_count}")
                    if len(df_nan_classes[cls]) > 0:
                        train_arrays.append(df_nan_classes[cls])
                        df_nan_classes[cls] = df_nan_classes[cls].iloc[0:0]  # Empty the dataframe

            # Safe concatenation to avoid axis=0 error with empty DataFrames
            print(f"DEBUG: train_arrays length: {len(train_arrays)}")
            for i, arr in enumerate(train_arrays):
                print(f"DEBUG: train_arrays[{i}] shape: {arr.shape}")
            non_empty_train_arrays = [df for df in train_arrays if not df.empty]
            df_train = pd.concat(non_empty_train_arrays) if non_empty_train_arrays else pd.DataFrame()
            print(f"DEBUG: Final df_train shape: {df_train.shape}")

            df_train, df_imputed = impute_processor(df_train, target)

            #remove any additional unused nan values for all classes
            for cls in unique_classes:
                array_df_removed.append(df_nan_classes[cls])


        #testing prevalance already set in front end, no further math needed based on settings
        test_counts = t['finalValues']['total']['test']

        #sample testing data with safety checks for all classes
        #must use string as key since passed as JSON
        print(f"DEBUG: test_counts: {test_counts}")
        for cls in unique_classes:
            print(f"DEBUG: Class {cls} shape before test sampling: {df_classes[cls].shape}")

        test_arrays = []
        
        # Safe sampling for all classes
        for cls in unique_classes:
            cls_str = str(cls)  # Convert to string for JSON key access
            test_count = test_counts.get(cls_str, 0)
            
            if test_count > 0 and len(df_classes[cls]) >= test_count:
                df_testing_class = df_classes[cls].sample(test_count, replace=False)
                test_arrays.append(df_testing_class)
                #remove testing data from pool
                df_classes[cls].drop(df_testing_class.index, inplace=True)
            elif test_count > 0 and len(df_classes[cls]) > 0:
                print(f"WARNING: Not enough class {cls} samples for testing. Available: {len(df_classes[cls])}, Required: {test_count}")
                test_arrays.append(df_classes[cls])
                df_classes[cls] = df_classes[cls].iloc[0:0]  # Empty the dataframe
            else:
                print(f"DEBUG: No class {cls} samples needed for testing or available")

        #put remaining data in removed
        for cls in unique_classes:
            array_df_removed.append(df_classes[cls])


        #combine testing data
        print(f"DEBUG: test_arrays length: {len(test_arrays)}")
        for i, arr in enumerate(test_arrays):
            print(f"DEBUG: test_arrays[{i}] shape: {arr.shape}")
        non_empty_test_arrays = [df for df in test_arrays if not df.empty]
        df_test = pd.concat(non_empty_test_arrays) if non_empty_test_arrays else pd.DataFrame()
        print(f"DEBUG: Final df_test shape: {df_test.shape}")

        #combined removed
        print(f"DEBUG: array_df_removed length: {len(array_df_removed)}")
        for i, arr in enumerate(array_df_removed):
            print(f"DEBUG: array_df_removed[{i}] shape: {arr.shape}")
        non_empty_removed_arrays = [df for df in array_df_removed if not df.empty]
        df_removed = pd.concat(non_empty_removed_arrays) if non_empty_removed_arrays else pd.DataFrame()
        print(f"DEBUG: Final df_removed shape: {df_removed.shape}")




        
        #file names defined at top of method

        #sort
        df_train = sort_values_original_order(df_train)
        df_test = sort_values_original_order(df_test)


        result.append(store_file_and_params(df_train, train_file_name, 'train'))
        result.append(store_file_and_params(df_test, test_file_name, 'test'))

        if df_removed.shape[0] > 0:
            #sort
            df_removed = sort_values_original_order(df_removed)
            result.append(store_file_and_params(df_removed, removed__file_name, 'removed'))

        try:
            #sort
            df_imputed = sort_values_original_order(df_imputed)
            result.append(store_file_and_params(df_imputed, imputed_file_name, 'imputed'))
        except:
            pass
    

    return result




        
    
        

def impute_processor(df, target):

        # Check if DataFrame is empty
        if df.empty:
            print("WARNING: Empty DataFrame passed to impute_processor")
            return df, pd.DataFrame()

        imp_mean = IterativeImputer(random_state=0)
        X = df.drop(columns=[target])
        y = df[target]

        imputed_row_index = list(df[df.isna().any(axis=1)].index)
        print(f"DEBUG: imputed_row_index: {imputed_row_index}")

        # If no rows need imputation, return original data
        if len(imputed_row_index) == 0:
            print("DEBUG: No rows need imputation")
            return df, pd.DataFrame()

        extra = df[['origin_file_name', 'origin_file_source_row']]
        X = X.drop(columns=['origin_file_name', 'origin_file_source_row'])

        # Check if X is empty after dropping columns
        if X.empty or len(X.columns) == 0:
            print("WARNING: No features available for imputation")
            return df, pd.DataFrame()

        #check if negative values exist in each column before imputation
        col_has_negative = ((X < 0).any()).to_dict()

        #flag columns for rounding
        col_is_binary = []
        col_is_numeric_cat = {}

        for col in X.columns:
            feature = X[col]
            
            if feature.isna().sum() > 0: #ensure has nan values
                unique = feature.dropna().unique()
                if len(unique) > 0:  # Check if unique values exist
                    unique.sort()
                    unique_int_len = len(list(filter(lambda x: x.is_integer(), unique))) #checks to ensure values are ints even if cast as float                    

                    if len(unique) == unique_int_len and (unique_int_len <= 20): #set 
                        col_is_numeric_cat[col] = unique

        try:
            imp_mean.fit(X)
            result = pd.DataFrame(imp_mean.transform(X),columns=X.columns, index=X.index)
            
            # Only round columns that actually have NaN values and exist in the result
            nan_columns = df.columns[df.isna().any()]
            existing_nan_columns = [col for col in nan_columns if col in result.columns]
            if existing_nan_columns:
                result[existing_nan_columns] = result[existing_nan_columns].round(decimals=3)

            #if column does not have negative values, change all imputed negative values to 0
            for col in col_has_negative:
                if col in result.columns and not col_has_negative[col]:
                    column = result[col]
                    column[column < 0 ] = 0
            
            # ensure numerical categorial data is maintained with imputation
            for col in col_is_numeric_cat.keys():
                if col in result.columns:
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

            # Safe access to imputed rows
            if len(imputed_row_index) > 0:
                # Filter imputed_row_index to only include indices that exist in result
                valid_indices = [idx for idx in imputed_row_index if idx in result.index]
                if valid_indices:
                    imputed = result.loc[valid_indices]
                else:
                    print("WARNING: No valid indices found for imputed rows")
                    imputed = pd.DataFrame()
            else:
                imputed = pd.DataFrame()

            return result, imputed
            
        except Exception as e:
            print(f"ERROR in impute_processor: {e}")
            print(f"DataFrame shape: {df.shape}")
            print(f"X shape: {X.shape}")
            print(f"Target: {target}")
            return df, pd.DataFrame()
