# coding: utf-8

# ---
#
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
#
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
#
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
#
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
#
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
#
# Rename the following list of countries (for use in later questions):
#
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
#
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,
#
# e.g.
#
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`,
#
# `'Switzerland17'` should be `'Switzerland'`.
#
# <br>
#
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**.
#
# Make sure to skip the header, and rename the following list of countries:
#
# ```"Korea, Rep.": "South Korea",
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
#
# <br>
#
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
#
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
#
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
#
# *This function should return a DataFrame with 20 columns and 15 entries.*


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## Dictionary
ContinentDict = {'China': 'Asia',
                 'United States': 'North America',
                 'Japan': 'Asia',
                 'United Kingdom': 'Europe',
                 'Russian Federation': 'Europe',
                 'Canada': 'North America',
                 'Germany': 'Europe',
                 'India': 'Asia',
                 'France': 'Europe',
                 'South Korea': 'Asia',
                 'Italy': 'Europe',
                 'Spain': 'Europe',
                 'Iran': 'Asia',
                 'Australia': 'Australia',
                 'Brazil': 'South America'}



### Question 1 (20%)
# Open and clean the datasets GDP, Energy, and ScimEn according to the guidance written at the beginning of this file.
# Join the three datasets into a new dataset (using the intersection of country names).
# Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
# *This function should return a DataFrame with 20 columns and 15 entries.*

## opening 1st file and cleaning it
energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38)  # open the file and remove the first 17 and last 38 rows
energy = energy.drop(energy.columns[[0, 1]], axis=1, inplace=False)  # delete the first 2 rows
energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']  # rename columns label
energy.replace('...', np.nan, inplace=True)  # replace ... with NaN
energy['Energy Supply'] *= 1000000

energy['Country'] = energy['Country'].str.replace('\d+', '')  # remove numbers from a string in a dataframe
energy['Country'] = energy['Country'].str.replace("\s*\(.*\)\s*",'')  # remove parentheses and all data within in a dataframe

energy['Country'] = (energy['Country'].replace({"Republic of Korea": "South Korea",
                                                "United States of America": "United States",
                                                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                                "China, Hong Kong Special Administrative Region": "Hong Kong"}))  # rename strings

## opening 2nd file and cleaning it
GDP = pd.read_csv('world_bank.csv', skiprows=4)  # open a csv file and remove the first 4 rows
GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                                   "Iran, Islamic Rep.": "Iran",
                                                   "Hong Kong SAR, China": "Hong Kong"})  # raname strings
GDP_filt = GDP.drop(GDP.iloc[:, 1:50], axis=1, inplace=False)  # drop all the columns except 'Country Name' and years from 2006 to 2015

## opening 3nd file
ScimEn = pd.read_excel('scimagojr-3.xlsx')  # open an excel file

## merging the 3 dataframes
df = pd.merge(pd.merge(ScimEn[0:16], energy, how='inner', left_on='Country', right_on='Country'), # merge ScimEn and energy dfs (only first 15 rows of ScimEn)
              GDP_filt, how='inner', left_on='Country',right_on='Country Name')  # merge the 2 dfs (ScimEn and energy) to ScimEn GDP
df = df.drop(['Country Name'], axis=1)  # drop column 'Country Name'
df.set_index('Country', inplace=True)  # making 'Country' column as an index

def answer_one():
    answer_1 = df
    print ('\nANSWER 1:\n',answer_1)
answer_one()



# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# *This function should return a single number.*

def answer_two():
    dfin = pd.merge(pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country'), # merge ScimEn and energy dfs (inner join)
           GDP_filt, how='inner', left_on='Country',right_on='Country Name')  # merge the 2 dfs (ScimEn and energy) to ScimEn GDP (inner join)
    dfin = dfin.drop(['Country Name'], axis=1)  # drop column 'Country Name'
    dfin.set_index('Country', inplace=True)  # making 'Country' column as an index

    dfout = pd.merge(pd.merge(ScimEn, energy, how='outer', left_on='Country', right_on='Country'), # merge ScimEn and energy dfs (outer join)
            GDP_filt, how='outer', left_on='Country', right_on='Country Name')  # merge the 2 dfs (ScimEn and energy) to ScimEn GDP (outer join)
    answer_2 = len(dfout) - len(dfin)
    print ('\nANSWER 2:',answer_2)
answer_two()



# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

def answer_three():
    global answer_3 # define answer_3 as a global variable since it will be used in Question 4
    answer_3 = df.iloc[:, 10:].mean(axis=1, skipna=True).sort_values(ascending=False)  # create a series with averaged GDP in the last 10 years (Question n 3)
    print('\nANSWER 3:\n',answer_3)
answer_three()



# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# *This function should return a single number.*

def answer_four():
    answer_4 = abs(df.loc[answer_3.index[5]].ix[10] - df.loc[answer_3.index[5]].ix[19])  # check the difference in between the last (2015) and first (2006) GDP value for the country having the 6th highest GDP
    print('\nANSWER 4:', answer_4)
answer_four()



# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# *This function should return a single number.*

def answer_five():
    answer_5 = df['Energy Supply per Capita'].mean()  # returns the mean Energy Supply per Capita
    print('\nANSWER 5:', answer_5)
answer_five()



# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# *This function should return a tuple with the name of the country and the percentage.*

def answer_six():
    answer_6 = df['% Renewable'].idxmax(), df['% Renewable'].max()  # returns a tuple with the country (index) having the highest % Renewable and its value
    print('\nANSWER 6:', answer_6)
answer_six()



# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations.
# What is the maximum value for this new column, and what country has the highest ratio?

def answer_seven():
    df['Citation_ratio'] = df['Self-citations'] / df['Citations']  # creates a new column from the ratio of 2 existing columns
    answer_7 = df['Citation_ratio'].idxmax(), df['Citation_ratio'].max()  # returns a tuple with the country (index) with the highest ration and the value of the ration
    print('\nANSWER 7:', answer_7)
answer_seven()



# ### Question 8 (6.6%)
# Create a column that estimates the population using Energy Supply and Energy Supply per capita.
# What is the third most populous country according to this estimate?

def answer_eight():
    df['Estimated_pop'] = (df['Energy Supply'] / df['Energy Supply per Capita'])  # creates a new column with the estimated population given by the ratio of Energy Supply and Energy Supply per capita
    answer_8 = df.sort_values('Estimated_pop', ascending=False).index[2]  # returns the name of the third highest estimated population
    print('\nANSWER 8:', answer_8)
answer_eight()



# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person.
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).

def answer_nine():
    df['Citable documents per Capita'] = (df['Citable documents'] / df['Estimated_pop'])  # creates a new column with the citable documents per capita
    answer_9 = df['Citable documents per Capita'].corr(df['Energy Supply per Capita'])  # returns the correlation in between 2 columns
    df.plot(x='Citable documents per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006], title='Answer 9') #creates a correlation data plot in between the 2 columns
    #plt.show()
    print('\nANSWER 9:', answer_9)
answer_nine()



# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

def answer_ten():
    mid = df['% Renewable'].median()
    df['HighRenew'] = df['% Renewable'] >= mid
    df['HighRenew'] = df['HighRenew'].apply(lambda x: 1 if x else 0)
    answer_10 = df.sort_values(by='Rank')
    answer_10 = answer_10['HighRenew']
    print('\nANSWER 10:\n', answer_10)
answer_ten()



# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

def answer_eleven():

    grouped = df['Estimated_pop'].groupby(ContinentDict)
    d = {'size': grouped.count(), 'sum': grouped.sum(), 'mean': grouped.mean(), 'std': grouped.std()}
    answer_11 = pd.DataFrame(data=d)
    answer_11 = answer_11[['size', 'sum', 'mean', 'std']]
    print('\nANSWER 11:\n', answer_11)
answer_eleven()



# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

df = df.reset_index()
def answer_twelve():
    #df = df.reset_index()
    df['Continent'] = [ContinentDict[country] for country in df['Country']]  # creates a column with the continent to which belong each country
    df['bins'] = pd.cut(df['% Renewable'], 5)  # creates a column with the binst of % Renewable
    answer_12 = df.groupby(['Continent', 'bins']).size()
    print('\nANSWER 12:\n', answer_12)
answer_twelve()



# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# e.g. 317615384.61538464 -> 317,615,384.61538464
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

def answer_thirteen():
    answer_13 = df.set_index('Country')  # set the column Country as index
    answer_13['PopEst'] = answer_13['Estimated_pop'].apply(lambda x: "{:,}".format(x))  # add the commas to the numbers
    answer_13 = answer_13['PopEst']
    print('\nANSWER 13:\n', answer_13)
    print('Junaid \nEffendi')
answer_thirteen()

