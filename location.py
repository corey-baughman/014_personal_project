# location.py

# location and gis functions for New Business Location Predictor

import geopandas as gpd
from shapely.geometry import Point
import os


def assign_census_tract():
    '''
    This function loads a census tract shapefile
    and to a DataFrame using geopandas. It then takes
    in latitude and longitude values of a location and
    prints what 2020 U.S. Census tract the location is
    in. See README for instructions to acquire shapefile.'''
    # Load census tract shapefile
    tracts = gpd.read_file('tl_rd22_48_tract')

    # Create point object
    point = Point( -98.49460900270131, 29.4192557501264)

    # Check if point is within a census tract
    tract = tracts[tracts.contains(point)]

    # Extract data from corresponding row in dataframe
    if not tract.empty:
        tract_data = tract.iloc[0]
        print("Point is within census tract:", tract_data['NAME'])
    else:
        print("Point is not within any census tract.")
