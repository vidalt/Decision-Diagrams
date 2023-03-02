"""
Module defining methods for each data pipeline operation.
"""

__author__ = "Pedro Martins"

import pandas as pd
from pandas.api.types import is_categorical_dtype

def replace(df, transformations):
    """
    Replace values in the DataFrame, if the `replace` transformation is defined.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    transformations : dict
        Transformation dictionary. If the `replace` key is present, its value is
        assumed to follow the dictionary structure:
        
        .. code:: python
            
            { old_value_1: new_value_1, old_value_2: new_value_2, ... } 
    """
    replace_dict = transformations.get('replace', None)
    if replace_dict == None:
        return df
    return df.replace(replace_dict)

def zero_index(df, transformations):
    """
    Replace original columns' 1-based indexing with 0-based indexing, if the `zero-index` 
    transformation is defined.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    transformations : dict
        Transformation dictionary. If the `zero-index` key is present, its value is
        assumed to be a list or range of column indexes to apply the operation.
    """
    zero_index_columns = transformations.get('zero-index', [])
    for column in zero_index_columns:
        df[column] = df[column].apply(lambda x: int(x) - 1)
    return df

def one_hot_encode(df, transformations):
    """
    Replace original columns' categorical values for one hot encoding (dummy variables), if the `one-hot-encode` 
    transformation is defined.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    transformations : dict
        Transformation dictionary. If the `one-hot-encode` key is present, its value is
        assumed to be a list or range of column indexes to apply the operation.
    """
    one_hot_columns = transformations.get('one-hot-encode', None)
    if one_hot_columns == None:
        return df
    for i in one_hot_columns:
        df[i] = pd.Categorical(df[i])
    # keeps the original column order
    columns = [
        pd.get_dummies(df[col], prefix=col, drop_first=True) if is_categorical_dtype(df[col]) else df[col] for col in df
    ]
    return pd.concat(columns, axis=1)

def drop_columns(df, transformations):
    """
    Remove whole columns from the DataFrame, if the `drop-columns` transformation is defined.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    transformations : dict
        Transformation dictionary. If the `drop-columns` key is present, its value is
        assumed to be a list or range of column indexes to apply the operation.
    """
    columns = transformations.get('drop-columns', [])
    return df.drop(columns, axis=1)

def drop_rows(df, transformations):
    """
    Remove whole rows from the DataFrame, if the `drop-rows` transformation is defined.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    transformations : dict
        Transformation dictionary. If the `drop-rows` key is present, its value is
        assumed to be a list or range of row indexes to apply the operation.
    """
    rows = transformations.get('drop-rows', [])
    return df.drop(rows, axis=0)

def drop_rows_with_values(df, transformations):
    """
    Remove whole rows from the DataFrame that contain the given value, if the `drop-rows-with-values` transformation is defined.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    transformations : dict
        Transformation dictionary. If the `drop-rows-with-values` key is present, its value is
        assumed to be a list of values. The special value `mean` will remove rows where the mean value
        was used as a data cleaning strategy for unknown values.
    """
    values = transformations.get('drop-rows-with-values', [])
    for value in values:
        if value == 'mean':
            df = _drop_rows_with_mean_value(df)
        else:
            df = df[df != value]
    return df

def _drop_rows_with_mean_value(df):
    """
    Remove rows where some cell value is the mean value of its column.

    This is useful for removing rows where the mean value was used as a data cleaning strategy for 
    unknown values.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    """
    for mean in df.mean():
        df = df[df != round(mean,6)]
    return df

def drop_missing_rows(df):
    """
    Remove whole rows from the DataFrame that have missing values.

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    """
    return df.dropna()

def rename_last_column_to_y(df):
    """
    Rename last column to `y` (standard name for the *target variables vector* in machine 
    learning data sets).

    Parameters
    ----------
    df : DataFrame
        DataFrame to transform.
    """
    return df.set_axis([*df.columns[:-1], 'y'], axis=1)
