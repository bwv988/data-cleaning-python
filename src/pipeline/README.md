# ETL Pipeline

The implementation of th ETL process is based on the Luigi framework: http://luigi.readthedocs.io/en/stable/index.html#

## Setup

```bash
$ pip install -r requirements.txt 
```

## Run ETL sketch

```bash
$ python pipeline.py
```

## Run Data cleaner sketch

The file `data_cleaner.py` contains a sketch of how to structure the cleaning process in practice. This should be implemented on top of Luigi.

```bash
$ python data_cleaner.py
```