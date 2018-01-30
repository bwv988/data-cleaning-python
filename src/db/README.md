# Database

This folder holds files to do with the Database.

For simplicity and brevity, I'm using containerized versions of Postgres and `pgadmin`.

In a production-grade setup with analytical BI query needs, a proper data warehouse, e.g. Amazon RedShift or Apache Ignite with replication / backup should be considered.

Also, we'd need a well-defined table structure based on access patterns in addition to proper data schemas.

## Setup

* Run `make setup` from project's top-level dir.
* Use `docker-compose` to start / stop DB and tooling.

## Usage

* Source Bash alias file: `$ source ./aliases.sh`.
* Start DB & `pgadmin` containers: 
    * `$ docker-compose up`
* Create DB:
    * `$ createdb -U postgres airlines_data`


* Now navigate to http://localhost:5050/browser/ to access `pgadmin`.
    * Use `admin / admin` as credentials.

* Add a new server in `pgadmin`:
    * Connection hostname: `db`
    * User: `postgres`
    * Password: `admin`

* Stopping containers: `$ docker-compose down`

## PSQL commands

```bash

# First, source alias.sh to use psql from command line.
source ./aliases.sh

psql

# Connect to DB 'airlines_data':

\c airlines_data

# List all relations:

\d

# Describe / verify table schemas

\dS+ airlines
\dS+ airports
\dS+ routes
```

## Create / drop database

```bash
# Drop
dropdb --if-exists -U postgres airlines_data

# Create
createdb -U postgres airlines_data
```

## Queries

```sql
-- Get all London Airports.
select * from airports where "Airport City" like '%London' and "Airport Country" like '%United Kingdom'

-- Get all London Airport IDs.
select * from airports a join routes r on a."Airport ID"=r."Destination Airport ID" where a."Airport ID"=492

-- How many routes do we have out of London, UK?
select count(*) from airports a 
	join routes r on a."Airport ID" = r."Source Airport ID" 
	where a."Airport ID" in
	(select "Airport ID" from airports where "Airport City" like '%London' and "Airport Country" like '%United Kingdom')
```