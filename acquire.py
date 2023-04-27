# acquire.py
import numpy as np
import pandas as pd

def get_sex_age_data():
    '''
    This function takes in 'sex_and_age.csv' from this
    repo (see README.md for how to get this file) and
    drops unnecessary columns as well as changing names
    to more pythonic and readable ones.
    
    Arguments: None
    Returns: DataFrame
    '''
    # read the file from the repo
    df = pd.read_csv('sex_and_age.csv', skiprows=[0,2])
    # establish chosen columns from the DataFrame
    sex_cols = ['Geography', 'Estimate!!Total!!Total population',
              'Estimate!!Total!!Total population!!SUMMARY INDICATORS!!Sex ratio (males per 100 females)',
              'Estimate!!Total!!Total population!!SUMMARY INDICATORS!!Old-age dependency ratio',
              'Estimate!!Total!!Total population!!SUMMARY INDICATORS!!Child dependency ratio']
    # redefine DataFrame as just the desired columns
    df = df[sex_cols]
    # make the column names pythonic and readable
    df.columns = [col.lower() for col in df.columns]
    df.columns = [col.replace('!!', '_') for col in df.columns]
    df.columns = [col.replace('estimate_total_', '') for col in df.columns]
    df.columns = [col.replace('summary indicators_', '') for col in df.columns]
    df.columns = [col.replace('total population_', '') for col in df.columns]
    # cut geography to the last six digits which are the census
    # tract id
    df.geography = df.geography.str[-6:]
    
    return df


def get_race_data():
    '''
    This function takes in 'race.csv' from this
    repo (see README.md for how to get this file) and
    drops unnecessary columns as well as changing names
    to more pythonic and readable ones
    
    Arguments: None
    Returns: DataFrame
    '''
    # read the file from the repo
    df = pd.read_csv('race.csv', skiprows=[0,2])
    # establish chosen columns from the DataFrame
    race_cols = ['Geography', ' !!Total:!!Hispanic or Latino']
    # redefine DataFrame as just the desired columns
    df = df[race_cols]
    # make the column names pythonic and readable
    df.columns = [col.lower() for col in df.columns]
    df.columns = [col.replace(' !!total:!!', 'total_') for col in df.columns]
    df.columns = [col.replace(' ', '_') for col in df.columns]
    
    # cut geography to the last six digits which are the census
    # tract id
    df.geography = df.geography.str[-6:]
    
    return df


def get_income_data():
    '''
    This function takes in 'income.csv' from this
    repo (see README.md for how to get this file) and
    drops unnecessary columns as well as changing names
    to more pythonic and readable ones
    
    Arguments: None
    Returns: DataFrame
    '''
    # read the file from the repo
    df = pd.read_csv('income.csv', skiprows=[0,2])
    # establish chosen columns from the DataFrame
    income_cols = ['Geography', 'Estimate!!Households!!Median income (dollars)']
    # redefine DataFrame as just the desired columns
    df = df[income_cols]
    # make the column names pythonic and readable
    df.columns = [col.lower() for col in df.columns]
    df.columns = [col.replace('!!', '_') for col in df.columns]
    df.columns = [col.replace(' !!total:!!', 'total_') for col in df.columns]
    df.columns = [col.replace(' ', '_') for col in df.columns]
    df.columns = [col.replace('estimate_', '') for col in df.columns]
    # cut geography to the last six digits which are the census
    # tract id
    df.geography = df.geography.str[-6:]
    
    return df


def get_census_data():
    '''
    Function takes in data from get_sex_age_data,
    get_race_data, and get_income_data and merges
    them into a single DataFrame.
    
    Arguments: None
    Returns: DataFrame
    '''
    df = pd.merge(pd.merge(get_sex_age_data(), get_race_data(), on='geography'), get_income_data(), on='geography')
    
    return df
