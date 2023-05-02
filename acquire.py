# acquire.py
# ============================================================


# IMPORTS:

# basic imports
import numpy as np
import pandas as pd
import os

# location/GIS imports
import geopandas as gpd
from shapely.geometry import Point

# imports to interact with google places API
import requests
import json

# local modules
from env import api # import API key
# ============================================================


# CENSUS DATA ACQUISITION:

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
    df = df.rename(columns={'Geography':'geography',
                            'Estimate!!Total!!Total population':'total_pop', 
                            'Estimate!!Total!!Total population!!SUMMARY INDICATORS!!Sex ratio (males per 100 females)': 'sex_ratio', 
                            'Estimate!!Total!!Total population!!SUMMARY INDICATORS!!Old-age dependency ratio':'old_age_dep_ratio', 
                            'Estimate!!Total!!Total population!!SUMMARY INDICATORS!!Child dependency ratio':'child_dep_ratio'})
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
    df = df.rename(columns={'Geography': 'geography',
                            ' !!Total:!!Hispanic or Latino':'total_hispanic_latino'})
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
    df = df.rename(columns={'Geography':'geography', 
                            'Estimate!!Households!!Median income (dollars)':'household_med_income'})
    # cut geography to the last six digits which are the census
    # tract id
    df.geography = df.geography.str[-6:]
    
    return df


def get_census_data():
    '''
    Function takes in data from get_sex_age_data,
    get_race_data, get_income_data and location.get_track_centroids
    and merges them into a single DataFrame.
    
    Arguments: None
    Returns: DataFrame
    '''
    df = pd.merge(pd.merge(pd.merge(get_sex_age_data(), get_race_data(), on='geography'), get_income_data(), on='geography')
                 , get_tract_centroids(), on='geography')
    df = df[df.total_pop != 0]
    df = df.astype(
        {'sex_ratio':'float','old_age_dep_ratio':'float', 
         'child_dep_ratio':'float','household_med_income':'int', 
         'centroid_lat':'float', 'centroid_long':'float'})
    df = df.reset_index(drop=True)
    
    return df

# ============================================================


#  GOOGLE PLACES DATA ACQUISITION:


def get_tract_centroids():
    '''
    Takes in the 2020 US Census Shapefile for Bexar County,
    TX and returns a df with geography number, centroid_latitude,
    and centroid longitude for each geography.
    See README for instructions to acquire shapefile.
    
    Arguments: None.
    
    Returns: DataFrame with columns 'geography', 'centroid_lat', 
    and 'centroid_long'.
    '''
    # Load census tract shapefile
    tracts = gpd.read_file('tl_rd22_48_tract')
    # select geography, centroid lat, centroid long
    df = tracts[(tracts.COUNTYFP == '029')]
    df = df[['TRACTCE', 'INTPTLAT', 'INTPTLON']]
    df = df.rename(columns={'TRACTCE':'geography', 
                     'INTPTLAT':'centroid_lat', 'INTPTLON':'centroid_long'})
    return df
    

def assign_census_tract(df):
    '''
    This function loads a census tract shapefile
    to a DataFrame using geopandas. It then takes
    in a DataFrame of latitude and longitude values and
    adds a column indicating what 2020 U.S. Census tract 
    each location is in or None if the location is not
    in Bexar County. Returns the DataFrame.
    See README for instructions to acquire shapefile.
    
    Arguments: DataFrame with columns 'latitude' and
    'longitude'.
    
    Returns: DataFrame with columns 'latitude', 'longitude',
    and 'census_tract'.
    '''
    # Load census tract shapefile
    tracts = gpd.read_file('tl_rd22_48_tract')
    # filter tracts to those in Bexar County
    tracts = tracts[(tracts.COUNTYFP == '029')]
    # convert df into a list of tuples
    coords = df.values.tolist()
    # add census tract column to df
    df['census_tract'] = None
    # Create point object
    for index, coord in enumerate(coords):
        point = Point(coord[1], coord[0])
        # Check if point is within a census tract
        tract = tracts[tracts.contains(point)]
        # Extract data from corresponding row in dataframe
        if not tract.empty:
            tract_data = tract.iloc[0]
            df.loc[index, 'census_tract'] = tract_data['NAME']
        else:
            df.drop(index=index, inplace=True)
            
    return df



def get_bexar_yoga_studios(api=api):
    '''
    This function searches google places API for yoga
    studios within 50km radius of the Bexar County 
    Courthouse. That includes all of Bexar County and
    may capture some area outside the county. Then filtration
    against census tract shapefiles is performed to remove
    results from outside the county. A google places API key
    is required for function use.
    
    Arguments: google places API key
    
    Returns: DataFrame of yoga studios in Bexar County, TX, USA.
    '''
    # set up API endpoint and parameters
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': '29.4241,-98.4936',  # Bexar County Courthouse, TX coordinates
        'radius': '50000',  # search radius in meters
        'keyword': 'yoga studio',  # keyword to search for
        'key': api  # replace with your own API key
    }

    # send HTTP request to API and get response
    response = requests.get(url, params=params)
    data = json.loads(response.text)

    # extract latitude and longitude coordinates for each result
    coordinates = []
    for result in data['results']:
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        coordinates.append((lat, lng))
        
    # convert coordinates to a pandas DataFrame
    df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
    
    # lookup census tract for each location
    df = assign_census_tract(df)
    
    # remove locations not in Bexar County and standardize
    # geography names
    df = clean_yoga_df(df)
    
    return df


def clean_yoga_df(df):
    '''
    Function takes in the output of get_bexar_yoga_studios()
    and removes any locations that are not in a Bexar County
    US Census tract. It also converts the census tract names
    to match the geography names in the census data.
    '''
    df = df[df.census_tract != None]
    df['geography'] = (
        (df.census_tract.astype('float')) * 100).astype('int').astype('str')
    df = df.drop(columns='census_tract')
    
    return df


def get_combined_data():
    '''
    Funtion takes in the dataframes from the census and
    also the one from Google Places and outputs a single
    DataFrame.
    '''
    df = pd.merge(get_census_data(), get_bexar_yoga_studios(), 
                  on = 'geography', how= 'left')
    df['has_yoga'] = df.latitude >= 0
    
    return df





# ============================================================