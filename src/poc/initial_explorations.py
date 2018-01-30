# Some initial explorations & data cleaning.
# RS1912018

#
# Load in raw data.
#
#%%
import pandas as pd
import numpy as np

#PROJ_PATH = "/Users/ralphschlosser/Dropbox/develop/data_project/"
PROJ_PATH = "/home/sral/Dropbox/develop/data_project/"

DATA_IN_PREFIX = "data/orig/"
DATA_OUT_PREFIX = "data/processed/"


airlines_raw = pd.read_excel(PROJ_PATH + DATA_IN_PREFIX + "20180102 Airlines.xlsx")
airports_raw = pd.read_excel(PROJ_PATH + DATA_IN_PREFIX + "20180102 Airports.xlsx")
routes_raw = pd.read_excel(PROJ_PATH + DATA_IN_PREFIX + "20180102 Routes.xlsx")


#%%
#
# Exploratory analysis.
#

airlines_raw.head()

## RES: First line looks dodgy. Remove?

all_dta = [airlines_raw, airports_raw, routes_raw]

## Print dimensions.
print("Dimensions...")
list(map(lambda x: print(x.shape), all_dta))

## Print types.
print("Data types...")
list(map(lambda x: print(x.dtypes), all_dta))

## RES: routes has the largest amount of entries, ~68k rows.
## Probably also the most scalable part of the data as new routes
## will be created, or existing ones updated.
## Need to understand unit of scale in new routes.

## Look at airline types.
print(airlines_raw.dtypes)

#%%
# What percentages of actual missing data do we have?
# Note: Missing means NaN; there are other types of flaws in the data which we'll get to later.

def print_perc_missing(df):
    """
    Prints what percentage of data is missing for each column.
    
    CAVEAT: Only checks for nan, not other data defects, e.g. "\\N" entries etc.
    """
    print(round(df.isnull().sum() / df.shape[0] * 100))
    
print("\nAirlines data\n")
print_perc_missing(airlines_raw)

## RES:
## Airline aliases flawed.
## Most IATA codes are rubbish. Many nan, and other issues.
## ICAO codes have nans and other problems.
## Further, 13% of airline callsigns are flawed.


#%%
print("\nAirports data\n\n")
print_perc_missing(airports_raw)
## Airport cities seems to be an issue. 
## Timezone offset too.
## NOTE: Some IATA codes are \N --> not NaN! Need to fix this too.
## Need to fix cities if we want to use it as a key.
## There are two unnamed columns. Could probably just delete those as they only contain NaNs.

#%%
print("\nRoutes data\n\n")
print_perc_missing(routes_raw)

## RES: Codeshare is totally useless. Rest seems OK for now.


#%%
#
# Data clearning / annotation.
#

# IMPL: 
# - Need to consider different cleaning strategies per column.
# - Some cleaning may have to be done manually. In other cases API access could help
# - to back-fill missing entries.
# - For example: https://www.icao.int/safety/iStars/Pages/API-Data-Service.aspx
# - But API access needs a subscription.


# Airports data
## Fix IATA / ICAO issue: Some entries are not nan but have a CRLF in it.
## Solution: Use regex!
## See: https://gist.github.com/yectep/4372d1166a192d5e9754
##
## Further, remove cols 13 and 14.

#%%

# Helper functions.
import re

def get_invalid_data(data, column_name, pattern):
    """
    This helper function returns a marker Series where True indicates
    invalid data, if the given regex pattern is NOT matched for a row in <column_name>.
    """
    compiled_pattern = re.compile(pattern)
    invalid_matcher = lambda x: bool(compiled_pattern.match(str(x)))
    return(data[column_name].apply(invalid_matcher))

def create_invalid_col_annotation(data, column_name, invalid_data):
    """
    This helper function creates a new column based on a marker series.
    """
    
    data["invalid_" + column_name] = invalid_data
    return(data)


def generic_str_strategy(data, col):
    """
    Generic cleaning strategy for null / nan data (String columns).
    """
    data.loc[data["invalid_" + col], col] = "MISSING"
    
#%%
# Clean airlines data.

def clean_airlines_data(data):
    """
    Invoke cleaning strategy for each column that needs cleaning.
    """
    clean_airlines_iata(data)
    clean_airlines_icao(data)
    clean_airlines_callsign(data)
    clean_airlines_country(data)
    clean_airlines_alias(data)
    
    # Drop first row.
    data = data.drop(0).reset_index(drop=True)
    
    return(data)
     
def clean_airlines_iata(data):
    """
    TBD
    """
    col = "IATA Code"
    create_invalid_col_annotation(data, col, get_invalid_data(data, col, "^(?![A-Z0-9]{2}).*"))
    generic_str_strategy(data, col)

def clean_airlines_icao(data):
    """
    TBD
    """
    col = "ICAO Code"
    create_invalid_col_annotation(data, col, get_invalid_data(data, col, "^(?![A-Z]{3}).*"))
    generic_str_strategy(data, col)


def clean_airlines_callsign(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Airline Callsign"
    invalid_callsigns = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_callsigns)
    generic_str_strategy(data, col)

def clean_airlines_country(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Airline Country"
    invalid_countries = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_countries)
    generic_str_strategy(data, col)

def clean_airlines_alias(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Airline Alias"
    invalid_alias = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_alias)
    generic_str_strategy(data, col)

#%%
#
# NOTE: Here we should also check if the things we use as index, e.g. Airline ID are unique!
    
airlines = clean_airlines_data(airlines_raw)

# Now all should be good (in terms of nan / null)
airlines.isnull().sum()

# Check that Airline ID is unique.
if not len(airlines["Airline ID"]) == len(np.unique(airlines["Airline ID"])): raise AssertionError()

#%%
# Clean airports data.

def clean_airports_data(data):
    """
    Clean airports data columns.
    """
    clean_airports_iata(data)
    clean_airports_icao(data)
    clean_latitude(data)
    clean_city(data)
    clean_tz_offset(data)
    clean_tz(data)
    clean_dst(data)
    
    # Drop nan columns
    data.drop(data.columns[[12, 13]], axis = 1, inplace = True)
    return(data)


def clean_airports_iata(data):
    """
    TBD
    """
    col = "IATA Code"
    
    create_invalid_col_annotation(data, col, get_invalid_data(data, col, "^(?![A-Z]{3}).*"))
    generic_str_strategy(data, col)    

def clean_airports_icao(data):
    """
    TBD
    """
    col = "ICAO Code"
    create_invalid_col_annotation(data, col, get_invalid_data(data, col, "^(?![A-Z]{4}).*"))
    generic_str_strategy(data, col)    

def clean_city(data):
    """
    This is actually crucial because we want to use City as a key!
    
    Also, this particular column seems to be a mess.
    
    Real-world considerations:
        - UTF conversion issues?
        - Invalid values....
    """
    col = "Airport City"
    invalid_city = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_city)
    generic_str_strategy(data, col)


def clean_tz_offset(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Timezone Offset"
    invalid_tz_off = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_tz_off)
    generic_str_strategy(data, col)

def clean_tz(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Timezone"
    invalid_tz = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_tz)
    generic_str_strategy(data, col)

def clean_dst(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "DST"
    invalid_dst = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid_dst)
    generic_str_strategy(data, col)

def clean_latitude(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Latitude"
    inv = data[col].isnull()
    create_invalid_col_annotation(data, col, inv)
    generic_str_strategy(data, col)


#%%
# Get clean airports data.
airports = clean_airports_data(airports_raw)

# Should yield all 0.
airports.isnull().sum()
    
#%%
# Clean routes data.

## There are issues with the equipment column.
## We want to be able to query for equipment type, so we need it as a separate column.
## Strategy: Create column for each aircraft of boolean type
## indicating if this equipment is being used, or not (True / False).
## NOTE: Source and Destination airport appear to be in IATA.

def clean_routes_data(data):
    """
    Invokes all the column cleaning strategies for the routes data.
    """
    data = clean_equipment(data)
    clean_airline(data)
    clean_destination_airport(data)
    clean_codeshare(data)
    clean_no_stops(data)
    data = clean_source_airport_id(data)
    data = clean_destination_airport_id(data)
    return(data)
    

def clean_airline(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Airline"
    invalid = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid)
    generic_str_strategy(data, col)    
    
def clean_destination_airport(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Destination Airport"
    invalid = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid)
    generic_str_strategy(data, col) 
    
def clean_codeshare(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "Codeshare?"
    invalid = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid)
    generic_str_strategy(data, col)  

def clean_no_stops(data):
    """
    FIXME: This only filters out nan values, not *all* incorrect values!
    """
    col = "No Stops"
    invalid = data[col].isnull()
    create_invalid_col_annotation(data, col, invalid)
    generic_str_strategy(data, col)  

def clean_equipment(data):
    """
    This function cleans the equipment column.
    """
    
    # Convert this column to a string type.
    data = data.astype({"Equipment": np.str})
    
    # Flatten a nested list.
    # FIXME: Should consider using itertools for Python >= 2.6
    # https://docs.python.org/3/library/itertools.html#itertools.product
    flatten = lambda l: [item for sublist in l for item in sublist]

    equip_raw = data["Equipment"]

    # Generate a list of unique equpment types.
    # FIXME: Might need to consider more than one space; remove empty strings / nan.
    equip_raw = [e.split(" ") for e in equip_raw]    
    equip = np.unique(flatten(equip_raw))
    equip[(equip == "") |  (equip == "nan")] = "MISSING"
    
    # Generate column names.
    prepend_eq = np.vectorize(lambda x: "eq_" + x)
    equip_cols = prepend_eq(equip)
    
    # Now add a boolean column for each eq. type.
    tmp = data.reindex(columns = equip_cols)
    tmp.fillna(value = False, inplace = True)
    tmp = tmp.astype(np.bool)
    
    # Join
    data.join(tmp)
    
    # Set to true if equip is present.
    # FIXME: Perhaps not the most elegant solution.
    for col in equip:
        data["eq_" + col] = data["Equipment"].str.contains(col)
    
    return(data)
    
def clean_airport_id(data, col_name):
    """
    Generic function to clean airport IDs.
    """
    non_num = re.compile("^(?![0-9]+).*")
    invalid_ids = lambda x: bool(non_num.match(str(x)))
    inv_ids = data[col_name].apply(invalid_ids)
    data.loc[inv_ids, col_name] =  "-1"
    # Convert to int!    

def clean_source_airport_id(data):
    """
    Clean the Source ID column, so we can use it as a key.
    """
    clean_airport_id(data, "Source Airport ID")
    return(data.astype({"Source Airport ID": np.int}))
    
def clean_destination_airport_id(data):
    """
    Clean the Destination ID column, so we can use it as a key.
    """
    clean_airport_id(data, "Destination Airport ID")
    return(data.astype({"Destination Airport ID": np.int}))
   
#%%
# Get clean routes data. 
routes = clean_routes_data(routes_raw)

routes.isnull().sum()


#%%

#
# Save processed (not yet fully cleaned data)
#
airlines.to_csv(PROJ_PATH + DATA_OUT_PREFIX + "airlines.csv", index = False)
airports.to_csv(PROJ_PATH + DATA_OUT_PREFIX + "airports.csv", index = False)
routes.to_csv(PROJ_PATH + DATA_OUT_PREFIX + "routes.csv", index = False)


#%%

#
# Ingest directly to database.
#
# FIXME: Should consider converting column names to exclude whitespaces.
# FIXME: Supply data schema.

# Note: May need to install additional packages:
# !conda install psycopg2

from sqlalchemy import create_engine

PSQL_HOST = "localhost"
PSQL_USER = "postgres"
PSQL_PW = "admin"
PSQL_PORT = "5432"
DB_NAME = "airlines_data"

DB_URL = "postgresql://" + PSQL_USER + ":" + PSQL_PW + "@" + PSQL_HOST + ":" + PSQL_PORT + "/" + DB_NAME

print("Connecting to PSQL URL: " + DB_URL)

# Create connection.
engine = create_engine(DB_URL)

# Dump data using default schema and name.
airlines.to_sql(name = "airlines", con = engine, if_exists = "replace")
airports.to_sql(name = "airports", con = engine, if_exists = "replace")

# This one will take a bit of time.
# FIXME: Supply schema!
routes.to_sql(name = "routes", con = engine, if_exists = "replace")

# Close connection.
con = engine.raw_connection()
con.close()

#%%
#
# Questions
#

# 1. Which aircraft type is the most common on routes out of London?
# Question: Does this mean London, UK? There is a London in the UK, Canada and US!

## Firstly, has any of the missing cities to do with London?
airports["Airport Name"].str.contains("London")
london_in_name = airports["Airport Name"].str.contains("London")
print(airports[london_in_name])
## Seemingly so, but wouldn't work with any city.
## Bottom line is City really needs to be cleaned properly.


## Get all the routes out of London.

## Issue here: Both City and Country might be flawed!
london_airport_ids = airports[(airports["Airport City"] == "London") & (airports["Airport Country"] == "United Kingdom")]["Airport ID"]

## Get all the routes out of London.
routes_out_of_london = routes[routes["Source Airport ID"].isin(list(london_airport_ids))]

## Get the most frequently used equipment type.
most_freq = routes_out_of_london.filter(regex = "^eq_.*").sum().sort_values(ascending = False)

## RES: A320
print(most_freq.head())

#%%
# 2. Which airline has the most routes into JFK?

## Need ID of destination JFK. We will use IATA.
## NOTE: This means IATA must be ok.
jfk_id = int(airports[(airports["IATA Code"] == "JFK")]["Airport ID"].values)

## Get all the airlines IDs with jfk_id as destination.
airline_ids_into_jfk = routes[routes["Destination Airport ID"] == jfk_id]["Airline ID"]

## Get ID with most flights.
most_routes_id = airline_ids_into_jfk.value_counts().index[0]

## Look up name.
## RES: Delta Airlines.
print(airlines[airlines["Airline ID"] == most_routes_id]["Airline Name"])


