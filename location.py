# location.py

# basic imports
import numpy as np
import pandas as pd

# location and gis functions for New Business Location Predictor

import geopandas as gpd
from shapely.geometry import Point
import os

# imports to interact with google places API
import requests
import json

# local modules
from env import api # import API key

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
            df.loc[index, 'census_tract'] = None
            
    return df



def get_bexar_yoga_studios(api):
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