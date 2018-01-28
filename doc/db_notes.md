# Some DB related notes.

## PSQL commands

```bash

# First, source alias.sh to use psql from command line.

# Connect to DB 'test'
\c test

# List all relations

\d

# Describe / verify table schemas

\dS+ airlines
\dS+ airports
\dS+ routes
```

## Create / Drop databas

```bash
# Drop
dropdb --if-exists -U postgres airline_data

# Create
createdb -U postgres airline_data
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