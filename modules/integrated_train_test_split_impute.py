
import pandas as pd
import numpy as np

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from .helpers import load_file, save_file, file_params, int_list_to_string, store_file_and_params, global_params

#LOCAL HELPERS

def normalize_class_key(cls):
    """Convert any class identifier to a consistent string format"""
    if isinstance(cls, (float, np.floating)) and cls.is_integer():
        return str(int(cls))  # 0.0 -> "0"
    elif isinstance(cls, (int, np.integer)):
        return str(cls)       # 0 -> "0"
    else:
        return str(cls)       # anything else -> string

def sort_values_original_order(df):
    # Check if the required columns exist before sorting
    if df.empty or 'origin_file_name' not in df.columns or 'origin_file_source_row' not in df.columns:
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
    describe = {}
    
    # Debug: Check if target column exists
    print(f"DEBUG merged_files_describe: Target column: {target}")
    print(f"DEBUG merged_files_describe: Available columns: {list(df.columns)}")
    print(f"DEBUG merged_files_describe: Target '{target}' in columns: {target in df.columns}")
    
    if target not in df.columns:
        raise KeyError(f"Target column '{target}' not found in dataframe during describe. Available columns: {list(df.columns)}")
    
    # Get all unique classes in the target column, excluding NaN values
    unique_classes = sorted(df[target].dropna().unique())
    
    # Ensure we only work with valid (non-NaN) target values for class analysis
    df_valid_target = df.dropna(subset=[target])

    #counts - only count valid target values (excluding NaN in target column)
    total_counts = df_valid_target[target].value_counts()
    total_df = pd.DataFrame({'counts': total_counts})
    total_df['percent'] = counts_to_percent(total_df)
    total_df.loc['total'] = total_df.sum() #make total row
    
    # Use consistent string keys throughout
    total_dict = total_df.to_dict()
    
    # Convert all class keys to consistent string format
    for key in ['counts', 'percent']:
        new_dict = {}
        # First copy the 'total' key if it exists
        if 'total' in total_dict[key]:
            new_dict['total'] = total_dict[key]['total']
        
        # Convert all class keys to strings using normalize_class_key
        for cls in unique_classes:
            if cls in total_dict[key]:
                cls_key = normalize_class_key(cls)
                new_dict[cls_key] = total_dict[key][cls]
        
        total_dict[key] = new_dict
    
    describe['total'] = total_dict

    #nan values - only consider rows where target is valid but other columns have NaN
    nan_rows = df[df.drop(columns=[target]).isna().any(axis=1) & df[target].notna()]
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
    
    # Use consistent string keys throughout
    nan_dict = nan_df.to_dict()
    
    # Convert all class keys to consistent string format
    for key in ['counts', 'percent']:
        new_dict = {}
        # First copy the 'total' key if it exists
        if 'total' in nan_dict[key]:
            new_dict['total'] = nan_dict[key]['total']
        
        # Convert all class keys to strings using normalize_class_key
        for cls in unique_classes:
            if cls in nan_dict[key]:
                cls_key = normalize_class_key(cls)
                new_dict[cls_key] = nan_dict[key][cls]
        
        nan_dict[key] = new_dict
    
    describe['nan'] = nan_dict

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
    
    # Use consistent string keys throughout
    non_nan_dict = non_nan_df.to_dict()
    
    # Convert all class keys to consistent string format
    for key in ['counts', 'percent']:
        new_dict = {}
        # First copy the 'total' key if it exists
        if 'total' in non_nan_dict[key]:
            new_dict['total'] = non_nan_dict[key]['total']
        
        # Convert all class keys to strings using normalize_class_key
        for cls in unique_classes:
            if cls in non_nan_dict[key]:
                cls_key = normalize_class_key(cls)
                new_dict[cls_key] = non_nan_dict[key][cls]
        
        non_nan_dict[key] = new_dict
    
    describe['non_nan'] = non_nan_dict

    # For multi-class, identify majority and minority classes (only from valid target values)
    class_counts = df_valid_target[target].value_counts()
    major = class_counts.idxmax()
    minor = class_counts.idxmin()

    # Store all unique classes for multi-class support (convert to regular Python types for JSON serialization)
    # Convert float classes to integers for consistency
    describe['unique_classes'] = []
    for cls in unique_classes:
        if isinstance(cls, (float, np.floating)) and cls.is_integer():
            describe['unique_classes'].append(int(cls))
        elif isinstance(cls, (int, np.integer)):
            describe['unique_classes'].append(int(cls))
        else:
            describe['unique_classes'].append(cls)
    describe['num_classes'] = len(unique_classes)
    describe['major'] = int(major) if isinstance(major, (int, np.integer)) else major
    describe['minor'] = int(minor) if isinstance(minor, (int, np.integer)) else minor

    print("=== BACKEND DESCRIBE DEBUG ===")
    print(f"unique_classes: {describe['unique_classes']}")
    print(f"total structure: {describe['total']}")
    print(f"nan structure: {describe['nan']}")
    print(f"non_nan structure: {describe['non_nan']}")
    print("=== END BACKEND DEBUG ===")

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



def apply_prevalence_adjustment(result, describe_obj, unique_classes, total_records):
    """Apply prevalence adjustment for multi-class support"""
    
    # Calculate original prevalences
    original_prevalences = {}
    for cls in unique_classes:
        cls_str = str(cls)
        original_prevalences[cls_str] = describe_obj['total']['counts'].get(cls_str, 0) / total_records if total_records > 0 else 0
    
    # Find limiting factor
    limiting_factor = float('inf')
    for cls in unique_classes:
        cls_str = str(cls)
        if original_prevalences[cls_str] > 0 and result['test']['counts'][cls_str] > 0:
            factor = result['test']['counts'][cls_str] / original_prevalences[cls_str]
            if factor < limiting_factor:
                limiting_factor = factor
    
    # Apply prevalence adjustment
    if limiting_factor != float('inf') and limiting_factor > 0:
        for cls in unique_classes:
            cls_str = str(cls)
            target_count = round(limiting_factor * original_prevalences[cls_str])
            excess = result['test']['counts'][cls_str] - target_count
            
            result['test']['counts'][cls_str] = max(0, target_count)
            if excess > 0:
                # Always use class-specific remainder structure
                if cls_str not in result['remainder']['counts']:
                    result['remainder']['counts'][cls_str] = 0
                result['remainder']['counts'][cls_str] += excess
    
    return result


def merge_files_segments(describe_obj, training_class_size, missing_values_option, prevelence_option):
    # Get all unique classes dynamically
    unique_classes = describe_obj.get('unique_classes', [])
    if not unique_classes:
        # Fallback to major/minor for legacy support
        unique_classes = [describe_obj['major'], describe_obj['minor']]
    
    # Initialize result structure with consistent class-based remainder
    result = {
        'train': {'counts': {}, 'percent': {}},
        'test': {'counts': {}, 'percent': {}},
        'remainder': {'counts': {}, 'percent': {}},
        'missing_values_option': missing_values_option,
        'prevelence_option': prevelence_option,
        'unique_classes': unique_classes
    }
    
    # Initialize remainder counts for each class
    for cls in unique_classes:
        cls_str = str(cls)
        result['remainder']['counts'][cls_str] = 0
    
    # Add legacy fields for backward compatibility
    if len(unique_classes) >= 2:
        result['major'] = unique_classes[0] if 'major' not in describe_obj else describe_obj['major']
        result['minor'] = unique_classes[1] if 'minor' not in describe_obj else describe_obj['minor']
    
    # Calculate total for percentage calculations
    total_records = 0
    for cls in unique_classes:
        cls_str = str(cls)
        total_records += describe_obj['total']['counts'].get(cls_str, 0)
    
    # Process each class
    for cls in unique_classes:
        cls_str = str(cls)
        
        # Handle both int and string keys for JSON compatibility
        try:
            total_count = describe_obj['total']['counts'].get(cls, 0)
            non_nan_count = describe_obj['non_nan']['counts'].get(cls, 0)
            nan_count = describe_obj['nan']['counts'].get(cls, 0)
        except:
            total_count = describe_obj['total']['counts'].get(cls_str, 0)
            non_nan_count = describe_obj['non_nan']['counts'].get(cls_str, 0)
            nan_count = describe_obj['nan']['counts'].get(cls_str, 0)
        
        # Calculate allocations based on missing values option
        if missing_values_option == 0:  # Remove missing values
            available_for_test = max(0, non_nan_count - training_class_size)
            remainder_from_missing = nan_count
        else:  # Impute missing values (missing_values_option == 1)
            available_for_test = max(0, total_count - training_class_size)
            remainder_from_missing = 0
        
        # Set training allocation
        actual_training_size = min(training_class_size, total_count)
        result['train']['counts'][cls_str] = actual_training_size
        
        # Set initial test allocation
        result['test']['counts'][cls_str] = available_for_test
        
        # Add missing values to remainder (class-specific)
        result['remainder']['counts'][cls_str] += remainder_from_missing
    
    # Apply prevalence adjustment if requested
    if prevelence_option == 1:
        result = apply_prevalence_adjustment(result, describe_obj, unique_classes, total_records)
    
    # Calculate percentages
    for cls in unique_classes:
        cls_str = str(cls)
        if total_records > 0:
            result['train']['percent'][cls_str] = round((result['train']['counts'][cls_str] / total_records) * 100, 1)
            result['test']['percent'][cls_str] = round((result['test']['counts'][cls_str] / total_records) * 100, 1)
            result['remainder']['percent'][cls_str] = round((result['remainder']['counts'][cls_str] / total_records) * 100, 1)
        else:
            result['train']['percent'][cls_str] = 0
            result['test']['percent'][cls_str] = 0
            result['remainder']['percent'][cls_str] = 0
    
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
            training_class_size = 25 #merge_files_training_class_size(describe_obj)
            groups_result[group]['training_class_size'] = training_class_size
            try:
                groups_result[group]['segments'] = merge_files_segments(describe_obj, training_class_size, 0, 1) #we don't actually use this now TODO
            except Exception as e:
                pass

           

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

    print(f"DEBUG: Starting transform_train_test_split_impute with target: {target}")

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
        
        print(f"DEBUG: Loaded file {file['name']} with columns: {list(df.columns)}")
        print(f"DEBUG: Target '{target}' in columns: {target in df.columns}")

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
            
            print(f"DEBUG: After concatenating {group} files:")
            print(f"DEBUG: Columns: {list(df.columns)}")
            print(f"DEBUG: Target '{target}' in concatenated dataframe: {target in df.columns}")
            print(f"DEBUG: DataFrame shape: {df.shape}")

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
                            # Not enough samples to drop for class {key}
                            pass

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
                            # Not enough test samples to drop for class {key}
                            pass
        
        # Safe concatenation to avoid axis=0 error with empty DataFrames
        non_empty_removed = [df for df in array_df_removed if not df.empty]
        df_removed = pd.concat(non_empty_removed) if non_empty_removed else pd.DataFrame()

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
        
        # Create dictionaries to hold class-specific dataframes
        df_classes = {}
        df_nan_classes = {}
        
        # Split data by class
        for cls in unique_classes:
            df_classes[cls] = df[df[target] == cls]
            df_nan_classes[cls] = df_classes[cls][df_classes[cls].isna().any(axis=1)]
        
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
                
                if len(df_classes[cls]) >= training_class_size:
                    df_training_class = df_classes[cls].sample(training_class_size, replace=False)
                    train_arrays.append(df_training_class)
                    #remove training data from original sample
                    df_classes[cls].drop(df_training_class.index, inplace=True)
                else:
                    if len(df_classes[cls]) > 0:
                        train_arrays.append(df_classes[cls])
                        df_classes[cls] = df_classes[cls].iloc[0:0]  # Empty the dataframe

            #combine training data
            non_empty_train_arrays = [df for df in train_arrays if not df.empty]
            df_train = pd.concat(non_empty_train_arrays) if non_empty_train_arrays else pd.DataFrame()

        #if impute missing value rows
        #TODO handle case if missing values > training class size
        elif missing_value_setting == 1:
            
            print(t)

            #remove missing values from non-nan data for all classes
            for cls in unique_classes:
                df_classes[cls] = df_classes[cls].drop(df_nan_classes[cls].index)
                print(f'class {cls}', df_classes[cls].shape)

            # CORRECT LOGIC: First sample test data (only from complete data), then training data
            test_counts = t['finalValues']['total']['test']
            test_arrays = []
            
            # Step 1: Sample test data first (only from complete non-NaN data)
            for cls in unique_classes:
                # Use consistent string key normalization
                cls_key = normalize_class_key(cls)
                test_count = test_counts.get(cls_key, 0)
                
                print(f"DEBUG: Class {cls} test sampling:")
                print(f"  - normalized key: {cls_key}")
                print(f"  - test_counts keys: {list(test_counts.keys())}")
                print(f"  - requested test samples: {test_count}")
                print(f"  - available complete samples: {len(df_classes[cls])}")
                
                if test_count > 0 and len(df_classes[cls]) >= test_count:
                    df_testing_class = df_classes[cls].sample(test_count, replace=False)
                    test_arrays.append(df_testing_class)
                    df_classes[cls].drop(df_testing_class.index, inplace=True)
                    print(f"  - sampled {test_count} test samples")
                elif test_count > 0 and len(df_classes[cls]) > 0:
                    test_arrays.append(df_classes[cls])
                    df_classes[cls] = df_classes[cls].iloc[0:0]
                    print(f"  - sampled all remaining {len(df_classes[cls])} samples")
                else:
                    print(f"  - no samples available for testing")

            train_arrays = []

            # Step 2: Sample training data from remaining complete data + NaN data for imputation
            for cls in unique_classes:
                # Use consistent string key normalization
                cls_key = normalize_class_key(cls)
                
                # Get counts from frontend calculations
                train_imputed_count = t['finalValues']['imputed']['train'].get(cls_key, 0)
                train_total_count = t['finalValues']['total']['train'].get(cls_key, 0)
                train_nonimputed_count = train_total_count - train_imputed_count
                
                print(f"DEBUG: Class {cls} training sampling:")
                print(f"  - train_total_count: {train_total_count}")
                print(f"  - train_imputed_count: {train_imputed_count}")
                print(f"  - train_nonimputed_count: {train_nonimputed_count}")
                print(f"  - available non-NaN samples after test: {len(df_classes[cls])}")
                print(f"  - available NaN samples: {len(df_nan_classes[cls])}")
                
                # Safety check: if frontend provides no training allocation, use default sampling
                if train_total_count == 0:
                    print(f"  - WARNING: Frontend provided 0 training samples for class {cls}, using fallback sampling")
                    # Use remaining data for training
                    fallback_nonimputed = len(df_classes[cls])
                    fallback_imputed = len(df_nan_classes[cls])
                    
                    actual_nonimputed_count = fallback_nonimputed
                    actual_imputed_count = fallback_imputed
                    
                    print(f"  - fallback: {actual_nonimputed_count} non-imputed + {actual_imputed_count} imputed = {actual_nonimputed_count + actual_imputed_count} total")
                else:
                    #sample training data minus missing values
                    actual_nonimputed_count = min(train_nonimputed_count, len(df_classes[cls]))
                    # Sample imputed training data
                    actual_imputed_count = min(train_imputed_count, len(df_nan_classes[cls]))
                
                if actual_nonimputed_count > 0:
                    df_training_class = df_classes[cls].sample(actual_nonimputed_count, replace=False)
                    df_classes[cls].drop(df_training_class.index, inplace=True)
                    train_arrays.append(df_training_class)
                    print(f"  - sampled {actual_nonimputed_count} non-imputed samples")
                
                if actual_imputed_count > 0:
                    df_train_impute = df_nan_classes[cls].sample(actual_imputed_count, replace=False)
                    df_nan_classes[cls].drop(df_train_impute.index, inplace=True)
                    train_arrays.append(df_train_impute)
                    print(f"  - sampled {actual_imputed_count} imputed samples")

            # Safe concatenation to avoid axis=0 error with empty DataFrames
            non_empty_train_arrays = [df for df in train_arrays if not df.empty]
            df_train = pd.concat(non_empty_train_arrays) if non_empty_train_arrays else pd.DataFrame()

            print(f"DEBUG: Final training dataframe before imputation:")
            print(f"  - Shape: {df_train.shape}")
            print(f"  - Columns: {list(df_train.columns) if not df_train.empty else 'EMPTY'}")
            print(f"  - Target column present: {target in df_train.columns if not df_train.empty else 'N/A'}")

            # Safety check: only call impute_processor if we have data
            if not df_train.empty and target in df_train.columns:
                df_train, df_imputed = impute_processor(df_train, target)
            else:
                print(f"WARNING: Empty training dataframe or missing target column, skipping imputation")
                df_imputed = pd.DataFrame()

            #remove any additional unused nan values for all classes
            for cls in unique_classes:
                array_df_removed.append(df_nan_classes[cls])


        # Combine testing data (already sampled above)
        non_empty_test_arrays = [df for df in test_arrays if not df.empty]
        df_test = pd.concat(non_empty_test_arrays) if non_empty_test_arrays else pd.DataFrame()

        #put remaining data in removed
        for cls in unique_classes:
            array_df_removed.append(df_classes[cls])

        #combined removed
        non_empty_removed_arrays = [df for df in array_df_removed if not df.empty]
        df_removed = pd.concat(non_empty_removed_arrays) if non_empty_removed_arrays else pd.DataFrame()

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
        imp_mean = IterativeImputer(random_state=0)
        
        # Debug: Check if target column exists
        print(f"DEBUG: Target column: {target}")
        print(f"DEBUG: Available columns: {list(df.columns)}")
        print(f"DEBUG: DataFrame shape: {df.shape}")
        
        if target not in df.columns:
            raise KeyError(f"Target column '{target}' not found in dataframe. Available columns: {list(df.columns)}")
        
        X = df.drop(columns=[target])
        y = df[target]

        imputed_row_index = list(df[df.isna().any(axis=1)].index)

        # If no rows need imputation, return original data
        if len(imputed_row_index) == 0:
            return df, pd.DataFrame()

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
                    imputed = pd.DataFrame()
            else:
                imputed = pd.DataFrame()

            return result, imputed
            
        except Exception as e:
            return df, pd.DataFrame()
