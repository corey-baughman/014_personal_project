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

def assign_census_tract(df):
    '''
    This function loads a census tract shapefile
    and to a DataFrame using geopandas. It then takes
    in a DataFrame of latitude and longitude values and
    adds a column indicating what 2020 U.S. Census tract 
    the location is in. Returns the DataFrame.
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
    df['census_tract'] = 'None'
    # Create point object
    for coord in coords:
        point = Point(coord[1], coord[0])
        # Check if point is within a census tract
        tract = tracts[tracts.contains(point)]
        # Extract data from corresponding row in dataframe
        if not tract.empty:
            tract_data = tract.iloc[0]
            df.census_tract = tract_data['NAME']
        else:
            df.census_tract = 'outside_bexar_county'
            
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
        
    # return coordinates as a pandas DataFrame
    return pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
