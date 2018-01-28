# Data Cleaning Project

## Description

Quick PoC for data cleaning / ingestion using Python.

## PoC Implementation notes:

* Data cleaning / processing using Pandas.
* Data pipeline implementation base: Luigi.
* Use of Postgres SQL for DB / data warehouse test.
* Canonical Juju for cloud-agnostic provisioning.

## Improvement Ideas

* Consider implementing Amazon Redshift or Apache Ignite for more scalable Data Warehouse.
    * Choice of exact technology depends largely on functional and non-functional requirements.
* Evaluate best-practices for Data Pipelines, e.g. as demonstrated here: https://github.com/groupon/luigi-warehouse

## Limitations

* No data schema handling / optimization. Should think how to best consolidate tables and DBs.
    * But this also depends on actual use cases.

## Links and References

### General
* Data schemas: https://frictionlessdata.io/
* Data Pipelines: https://www.slideshare.net/InfoQ/building-data-pipelines-in-python

### Luigi
* http://luigi.readthedocs.io/en/stable/
* https://www.slideshare.net/erikbern/luigi-presentation-nyc-data-science
* https://github.com/groupon/luigi-warehouse
