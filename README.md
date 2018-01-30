# Data Cleaning Project

## Description

Quick PoC for data cleaning / ingestion using Python.

## Implementation highlights

* Data cleaning and processing using Pandas.
* ETL pipeline implementation (sketch): *Luigi*.
* Use of *Postgres SQL* for DB / data warehouse PoC.
* Completely containerized setup.
* `cloud-init`-based bootstrapping of demo VM in Azure cloud.
* ExpressJS, React, Typescript-based web app (unfinished).

## Quickstart

The below commands will perform setup steps and run the environment on a docker host with `docker-compose` installed.

```bash
make setup
docker-compose up
source src/db/aliases.sh
createdb -U postgres airlines_data
```

### Jupyter

View the Data Cleaning and Ingestion PoC in a Jupyter notebook: http://localhost:8888/notebooks/Airlines%20Data%20Cleaning%20and%20Ingestion.ipynb

### Postgres

* Launch `pgadmin` UI: http://localhost:5050/
    * Use `admin/admin`.

* Add a new server in `pgadmin`:
    * Connection hostname: `db`
    * User: `postgres`
    * Password: `admin`

## Subfolders

* `src/db` - Contains scripts and notes on the Data Warehouse
* `src/pipeline` - A sketch of a Luigi-based ETL process plus some additional classes to show how the ETL should be implemented in production.
* `src/poc`- Python code and Jupyter notebook.
* `src/provisioning` - Notes and scripts for cloud provisioning.
* `src/webapp` - Web application.

## Improvement Notes

* Consider using Amazon Redshift or Apache Ignite for more scalable, tiered Data Warehouse.
* However choice of exact technology depends largely on functional and non-functional requirements, e.g. freqency of updates, read / write, availability, backups, etc.
* Evaluate best-practices for ETL pipelines, e.g. as demonstrated here: https://github.com/groupon/luigi-warehouse
* Use Canonical's Juju for cloud-agnostic provisioning.

## Limitations

* No data schema handling / optimization. Should think how to best consolidate tables and DBs.
* But this too depends on actual use cases.

## Links and References

### General
* Data schemas: https://frictionlessdata.io/
* Data Pipelines: https://www.slideshare.net/InfoQ/building-data-pipelines-in-python

### Luigi

* http://luigi.readthedocs.io/en/stable/
* https://www.slideshare.net/erikbern/luigi-presentation-nyc-data-science
* https://github.com/groupon/luigi-warehouse

### Other

Delete dangling docker images:

```bash
docker rmi $(docker images --quiet --filter "dangling=true")
```