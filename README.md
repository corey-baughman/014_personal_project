# 014_personal_project
**Repo for CodeUp Data Science Personal Project**

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

### Background

Census data had to be acquired from the U.S. Census Bureau. Below are instructions to retrieve that data.

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

## Acquire

* Three basic types of data were required:
    1. Census question data
    1. Census tract shapefile data
    1. Business search results data
* Select Census question data was acquired from U.S. Census Bureau website.
* Data was from the 2020 census.
* Data was downloaded as three .csv files and imported into pandas dataframes which were combined on census tract number a.k.a. 'geography'
* The data was limited to Bexar County, TX which has 375 census tracts. Each of these represents a row.
* The census tract shapefiles were required to assign point from search data into census tracts.
* The shapefiles were also retrieved from the U.S. Census Bureau website.
* Business search results data was retrieved using the Google Places API.
* Geopandas was then used to assign the locations retrieved to census tracts.

## Prepare

#### Data Cleaning Steps:
- Used following to clean data:
    1. Renamed columns to readable, pythonic names for each DataFrame.
    2. Standardized Geography names across DataFrames
    3. Dropped Columns from Census question DataFrames to select an initial feature set. (Entire tables must be downloaded as .csv and many features are heavily subsetted)
    4. Combined three census question DataFrames on 'geography' which was standardized and had 375 rows for every DataFrame.
    5. There were four federal tracts that had total populations of zero and those were dropped.
    6. Search results from Google Places were checked against census tracts to verify they were in Bexar County else they were dropped. 
    7. There were a total of 13 yoga studios in the county.
    8. Chose to ignore outliers for simplicity in the MVP and since underlying distibutions were not heavily skewed.
    9. There were no null values other than the four zero population tracts.

## Exploration

#### Insights from Univariate Exploration:

    1. Features are relatively normally distributed.
    2. Target classes are heavily imbalanced
    1. The sample size for the target is very small
    
#### Insights from Bivariate Exploration:

    1. There are slight positive correlations between having a yoga studio and income as well as being further north geograpically
    2. There is a slight negative correlation between having a yoga studio and the child dependency ratio.
    

#### Clustering Summary:

- visually, there are no distinct clusters at k=3 to k=7
- will add clusters with k=5 as a feature for modeling anyway.


### Exploration Summary: What Drives Studio Placement?
1. higher household median income
2. placement further north in the county
3. lower child dependency ratio
4. Initial clustering exploration did not produce strong clusters visually

## Modeling

#### **Goal:** The goal of my modeling phase is to build a model that predicts whether a census tract will have a yoga studio.
    
#### **Evaluation**: Models will be evaluated by the recall metric:
    1. against a baseline model by accuracy
        - accuracy measures total number of correct predictions over the total number of observations. It is a useful measure against the baseline model
    2. against each other using recall
        - recall measures the number of True Positive Predictions divided by total number of actual positive observations. I'm using it because I want to cast a wide net for areas that may be good candidates for a studio. It can't be checked against baseline, but is the best measure for these models against each other.
        
#### The baseline model is created by replacing all predicted values with the most common class from the actual values. In this case that is 'False' for no yoga studio in the census tract.

### Modeling Wrap 
* With an accuracy of .96 and a recall of 0.00 for the True class, the current Random Forest Classifier model fails to beat the baseline model of guessing 'no studio' for any given census tract.

## Conclusion

### Summary
* Some drivers of business placement were found
* The current classification model fails to beat baseline 


### Next Steps
1. Add features that measure distance between studios and tract centroids
2. Explore other algorithms for modeling
3. Test with a larger dataset
4. Work on balancing classes