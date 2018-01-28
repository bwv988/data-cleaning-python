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
