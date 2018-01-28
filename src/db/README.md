# Database

This folder contains files to do with the Database.

For simplicity, I'm using containerized versions of Postgres and `pgadmin`.

## Setup

* Run `make setup` from project's top-level dir.
* Use `docker-compose` to start / stop DB and tooling.

## Usage

* Source Bash alias file: `$ source ./aliases.sh`.
* Create DB:
    * `$ createdb -U postgres airlines_data`
* Start DB & `pgadmin` containers: `$ docker-compose up`


* Now navigate to http://localhost:5s050/browser/ to access `pgadmin`.
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

## Create / Drop databas

```bash
# Drop
dropdb --if-exists -U postgres airlines_data

# Create
createdb -U postgres airlines_data
```

## Queries

```sql
select * from airports where "Airport City" like '%London' and "Airport Country" like '%United Kingdom'


select * from airports a join routes r on a."Airport ID"=r."Destination Airport ID" where a."Airport ID"=492

select count(*) from airports a 
	join routes r on a."Airport ID" = r."Source Airport ID" 
	where a."Airport ID" in
	(select "Airport ID" from airports where "Airport City" like '%London' and "Airport Country" like '%United Kingdom')
```