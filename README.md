# 014_personal_project
Repo for CodeUp Data Science Personal Project

Project Goal:

Create a model that uses census tract data for Bexar County and Google search of existing businesses to predict where to put a new business of that type.

Plan of Attack:

- basic structure of program:
    - acquire census tract shape files for Bexar County, Texas from census.gov.
    - acquire some basic census features by census tract and import into a data frame
    - find geographic center of each census tract and assign all data for the tract to that point.
    - figure out how to use Google Places API to return coordinates of business type being searched for, e.g., 'yoga studio', 'coffee shop', 'mechanic'.
    - use geopandas and census tracts to assign each of those search results to a census tract
    - add a column to DataFrame 'has_feature' to show where there are current businesses.
    - Census tract number should be the 'primary key' of this dataset: i.e. each row is a census tract and each column is a feature of that tract.
    - Use distance based modeling to predict where there are studios and compare to where there are actually studios.
    - What sort of model would work best for this? Regression would be able to predict? This seems like a perfect application for KMeans Clustering. So need to make all of the features continuous.

Census Links:

TIGER/Line Shapefiles: The TIGER/Line Shapefiles contain geographic data for the United States, including census tract boundaries. These files are available for download from the Census Bureau's website at https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html.
American Community Survey (ACS) data: The ACS provides detailed demographic and socioeconomic data for census tracts, including population, race, ethnicity, income, and more. ACS data can be accessed and downloaded from the Census Bureau's website at https://www.census.gov/programs-surveys/acs/data.html.
Census Bureau API: The Census Bureau also provides an API that can be used to access census tract data programmatically. The API provides access to a wide range of demographic and socioeconomic data for census tracts, as well as other geographic units. Information on accessing the API can be found at https://www.census.gov/data/developers/data-sets/popest-popproj/popest.Vintage_2019.html.

Bexar County is C48029

Retrieving Census Data:

Census Block Groups:
    A Census Block Group is a geographic unit used by the United States Census Bureau for statistical purposes. It is a subdivision of a Census Tract and typically consists of between 600 and 3,000 people, although the exact size varies by location.

Census Block Groups are used to provide more detailed demographic and socioeconomic data than can be obtained at the Census Tract level. They are often used by researchers, planners, and policymakers to analyze population characteristics and trends, such as income, education, housing, and employment. Census Block Groups are also used for redistricting, marketing, and other purposes that require detailed demographic information.

Census Block Groups are identified by a unique 12-digit code, which is based on the State FIPS code, the County FIPS code, the Census Tract code, and the Block Group number. For example, the first two digits of the code represent the State FIPS code, the next three digits represent the County FIPS code, the next six digits represent the Census Tract code, and the final digit represents the Block Group number. The code allows Census Block Groups to be easily identified and compared across different geographic areas.

Data Acquisition:

Population and Sex Data:
1. Navigate to following link:
https://data.census.gov/table?g=050XX00US48029,48029$1400000&y=2020
1. click on the 'Download Table' link
1. From the downloaded .zip file, select 'ACSST5Y2020.S0701-Data.csv'.
1. Rename the file 'sex_and_age.csv'.
1. Move 'sex_and_age.csv' to the repo directory.


Race Data:
1. Navigate to following link: 
https://data.census.gov/table?t=Race+and+Ethnicity&g=050XX00US48029,48029$1400000&y=2020
1. Click on the small 'Download Table Data' link.
1. From the downloaded .zip file, select 'DECENNIALPL2020.P2-Data.csv'.
1. Rename the file 'race.csv'.
1. Move 'race.csv' to the repo directory.

Income Data:
1. Navigate to following link:
https://data.census.gov/table?t=Income+and+Poverty&g=050XX00US48029,48029$1400000&y=2020&tid=ACSST5Y2020.S1901
1. Click on the 'Download Table' link
1. From the .zip file, select 'ACSST5Y2020.S1901-Data.csv'.
1. Rename the file 'income.csv'.
1. Move 'income.csv' to the repo directory.

Census Tract Shapefile:
1. Navigate to following link:
https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/48_TEXAS/48/
1. Click on the 'tl_rd22_48_tract.zip' link
1. From the .zip file, select the 'tl_rd22_48_tract' folder.
1. Move the 'tl_rd22_48_tract' folder to the repo directory.

env.py file:
1. You must create a file named env.py in the repo directory.
1. The file must contain the following line of code with a valid Google Places API key substituted where noted:

``` api = 'Replace with Google Places API key' '''

