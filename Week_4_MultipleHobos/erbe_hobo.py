# -*- coding: utf-8 -*-

import pandas as pd


def get_time_column(columns):
    """Returns the time column from a list of Hobo headers
    
    Arguments:
        - columns (str): list of column names
        
    Returns
        - str: the time column name
    
    """
    return columns[1]


def decompose_column_name(col_name):
    """Returns separate parts of a hobo column name
    
    Argument:
        - col_name (str): the column name
        
    Returns:
        - tuple: (variable_name, unit_name, serial_text)
    
    """
    
    x=col_name.split('(')
    
    try:
        serial_text=x[1].split(')')[0].strip()
    except IndexError:
        serial_text=None    
    
    y=x[0].split(',')
    variable_name=y[0].strip()
    
    if len(y)>1:
        unit_name=y[1].strip()
    else:
        unit_name=None
    
    return variable_name,unit_name,serial_text


def read_hobo_file(filename,convert_to_farenheit=False):
    """
    
    Arguments:
        - filename (str): the name of the hobo file
        
    Returns:
        - pd.DataFrame
    
    """
    
    print(filename)
    
    # find the time column
    df=pd.read_csv(filename,skiprows=1)
    time_zone=get_time_column(df.columns)
    
    # read in the csv
    df=pd.read_csv(filename,skiprows=1,parse_dates=[time_zone])
    
    # set the index as the time column
    df=df.set_index(time_zone)
    
    # rename columns
    columns=[decompose_column_name(x) for x in df.columns]
    df.columns=pd.MultiIndex.from_tuples(columns)
    
    df.columns=df.columns.set_names(['variable_name','units','serial_text'])
    
    # convert temperatures to farenheit
    if convert_to_farenheit:
        try:
            df1=df['Temp']['°F']
            for col in df1.columns:
                df=farenheit_to_centigrade(df,('Temp','°F',col))
        except KeyError:
            pass
    
    return df


def farenheit_to_centigrade(df,column_name):
    """Converts the data in column_name from F to C
    
    Arguments
        - df (pd.Dataframe)
        - column_name (str)
        
    returns
        - (pd.Dataframe) - the updated dataframe
    
    """
    
    if column_name[1]!='°F':
        raise Exception('The units are not farenheit')
    
    df[column_name[0],'°C',column_name[2]]=(df[tuple(column_name)]-32)*5/9
    
    
    return df

