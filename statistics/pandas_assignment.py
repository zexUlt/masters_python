import os
import pandas as pd
import json


__COLUMNS__ = list(str())
__OUTPUT__ = str()
__CONFIG__ = 'config.json'


def generate_filename(filepath: str, suffix='') -> str:
    """This function generates filename for statfile in this task
        according to test case filename

    Args:
        filepath (str): filepath to test cases 
        suffix (str, optional): Suffix to append to filename. Defaults to ''. 

    Returns:
        str: Generated filename
    """

    return os.path.join(__OUTPUT__, 'statfile_' + os.path.split(filepath)[1].split('_')[2][-2:] + suffix + '.tsv')


def task_1(df: pd.DataFrame) -> pd.DataFrame:
    """This function solves the first part of this task -- a calculation of several statistics metrics

    Args:
        df (pd.DataFrame): Dataframe with source data

    Returns:
        pd.DataFrame: Dataframe with needed metrics
    """
    
    grouped = df.groupby('EVENT')

    my_min = grouped.min()
    med = grouped.median()
    q9  = grouped.quantile(q=.9)
    q99  = grouped.quantile(q=.99)
    q999  = grouped.quantile(q=.999)
    
    out = pd.merge(left=my_min, right=med, left_on='EVENT', right_on='EVENT').merge(
            right=q9, left_on='EVENT', right_on='EVENT').merge(
            right=q99, left_on='EVENT', right_on='EVENT').merge(
            right=q999, left_on='EVENT', right_on='EVENT')
    
    print_template = 'min={} 50%={} 90%={} 99%={} 99.9%={}'.format
    out = out.apply(lambda x: print_template(*x), axis=1).str.split(pat=' ', expand=True)

    return out


def task_2(df: pd.DataFrame) -> pd.DataFrame:
    """This function solves the second part of this task -- a table construction

    Args:
        df (pd.DataFrame): Dataframe with source data

    Returns:
        pd.DataFrame: Calculated dataframe according the task
    """

    # Calculating first and second columns 'EXEC_TIME' and 'TRANS_NO' respectively
    out_df = df.rename(columns = {'AVGTSMR': "exec_time"}).drop('EVENT', axis=1)
    out_df = out_df[out_df['exec_time'] % 5 == 0].groupby(by='exec_time', as_index=False).agg(trans_no=('exec_time', 'size'))
    # Third column 'WEIGHT'
    out_df['weight'] = round(out_df['trans_no'] / df.size * 100, 2)
    # And the last one 'PERCENT'
    out_df.insert(out_df.columns.size, 'percent', [df[df['AVGTSMR'] <= row['exec_time']].size / df.size * 100 for i, row in out_df.iterrows()]) 
    
    return out_df


def process_test_case(test_file: str):
    """This is the main function, where source data grabbed and calculations invoked.

    Args:
        test_file (str): Path to file with source data
    """

    main_df = pd.read_csv(test_file, sep='\t', usecols=__COLUMNS__, skipfooter=2, skiprows=2, engine='python')
    
    out1 = task_1(main_df)
    out2 = task_2(main_df)

    out1.to_csv(generate_filename(filepath=test_file), sep='\t', header=False)
    out2.to_csv(generate_filename(filepath=test_file, suffix='_2'), sep='\t', header=True)
    
        
    

if __name__ == '__main__':
    # First parse config file
    with open(__CONFIG__) as cfd_fd:
        cfg_json = cfd_fd.read()

    cfg = json.loads(cfg_json)    

    # Fill in all necessary variables
    test_dir = cfg['tests']['root']
    samples = cfg['tests']['samples']
    __OUTPUT__ = cfg['settings']['output']
    __COLUMNS__ = cfg['settings']['columns']

    # Processing each file in testing directory 
    for root, dirs, files in os.walk(test_dir + samples):
        for file in files:
            process_test_case(os.path.join(root, file))
