"""
Pipeline for processing raw ARFF data sets into CSV files in a standard format.

Used to process all 54 data sets needed for the experiments in the original paper.
"""

__author__ = "Pedro Martins"

from argparse import ArgumentParser
from pathlib import Path
import os
import arff, pandas as pd

from transformations import dataset_transformations
from operations import (replace, drop_rows_with_values, drop_missing_rows, 
    zero_index, one_hot_encode, drop_columns, drop_rows, rename_last_column_to_y)

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('dataset', nargs='?', help='Data set name to process. Must match the filename (without extension)\
        of a *.arff* file in the ``datasets/raw`` directory. Alternatively, use ``all`` or omit to process all datasets.')
    parser.add_argument('-f', '--force', help='Overwrites existing processed files.', action='store_true')
    parser.add_argument('-d', '--debug', help='Enters debug mode, does not output file.', action='store_true')
    parser.add_argument('-p', '--print-only', help='Prints result, does not output file.', action='store_true')
    return parser

def run():
    args = arg_parser().parse_args()

    if not os.path.exists(full_filepath('processed')):
        os.mkdir(full_filepath('processed'))

    process_all = args.dataset == 'all' or args.dataset == None
    dataset_names = dataset_transformations.keys() if process_all else [args.dataset]

    for name in dataset_names:
        process(name, force=args.force, debug=args.debug, print_only=args.print_only)

def process(dataset_name, force=False, debug=False, print_only=False):
    transformations = dataset_transformations.get(dataset_name, {})
    raw_filepath = full_filepath('./raw/{}.arff'.format(dataset_name))
    processed_filepath = full_filepath('./processed/{}.csv'.format(dataset_name))

    if not (force or debug or print_only) and os.path.exists(processed_filepath):
        print('{} dataset already processed'.format(dataset_name))
        return
    
    df, error = load_arff_dataframe(raw_filepath, dataset_name)
    if error:
        return

    df_processed = (df
        .pipe(replace, transformations)
        .pipe(drop_rows_with_values, transformations)
        .pipe(drop_missing_rows)
        .pipe(zero_index, transformations)
        .pipe(one_hot_encode, transformations)
        .pipe(drop_columns, transformations)
        .pipe(drop_rows, transformations)
        .pipe(rename_last_column_to_y)
    )

    if debug or print_only:
        print(df_processed)
        if debug: import pdb; pdb.set_trace()
    else:
        df_processed.to_csv(processed_filepath, index=False, header=True)

def load_arff_dataframe(filepath, dataset_name):
    try:
        with open(filepath, 'rt') as arff_file:
            arff_dataset = arff.loads(arff_file)
            return pd.DataFrame(arff_dataset['data']), False
    except FileNotFoundError:
        print('{} not found in `raw` folder'.format(dataset_name))
        return None, True

def full_filepath(relative_path):
    return (Path(__file__).parent / relative_path).resolve()

if __name__ == '__main__':
    run()