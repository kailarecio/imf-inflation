'''this script cleans raw data file exported from IMF database for PCA and exports it in csv format for further analysis on R'''

import pandas as pd
import yaml

# read yaml file
with open('countries.yaml', 'r') as file:
    country_dict = yaml.safe_load(file)

# import inflation data from IMF csv file
inflation = pd.read_csv('inflation.csv', index_col=0)

# keep monthly yoy changes in inflation
yoy_inflation_monthly = inflation[(
                            inflation['TYPE_OF_TRANSFORMATION'] == 'Period average, Year-over-year (YOY) percent change') & 
                            (inflation['FREQUENCY'] == 'Monthly'
                             )]

# drop columns where all values are na
yoy_inflation_monthly = yoy_inflation_monthly.dropna(how='all', axis=1)
yoy_inflation_monthly.drop(columns=['SERIES_CODE', 'OBS_MEASURE', 'INDEX_TYPE', 'TYPE_OF_TRANSFORMATION', 'FREQUENCY', 'SCALE'], inplace=True)

yoy_inflation_monthly.columns = yoy_inflation_monthly.columns.str.lower()

# melt to long: country / category / date / inflation
long_headline = yoy_inflation_monthly.melt(
    id_vars=['country', 'coicop_1999'],
    var_name='date',
    value_name='yoy_inflation'
)

long_headline["date"] = pd.to_datetime(long_headline["date"].str.replace("-m", "-"), format="%Y-%m")

# 1 column per category for PCA
headline_categories = long_headline.pivot_table(index=['country','date'],
                                                columns='coicop_1999',
                                                values='yoy_inflation')
headline_categories = headline_categories.reset_index()

# select countries and dates
for_pca = headline_categories[(headline_categories['country'].isin(country_dict['countries'])) &
                              (headline_categories['date'] < '2026-01-01')]

# export to csv for R
for_pca.to_csv('headline_all_cats.csv')