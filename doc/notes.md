# Project Dvelopment Notes and Links

## General Notes

### Data
* Write down assumptions.
* Choose in memory data warehouse, because it's not big data, so need fast queries.
    * Apache Ignite? https://ignite.apache.org/
    * Doesn't really have a good Python interface / perhaps too complicated for now.

* Cleaning: Can fix data problems if required using aux sources (e.g. filling in airline names) but not necessarily if, for example, the info is redundant, or not required for application.
* Need to fix some data problems in order to answer questions.
* Should consider data schemas: https://frictionlessdata.io/
* Building data pipelines: https://www.slideshare.net/InfoQ/building-data-pipelines-in-python
* How to handle data schemas in Python? 
* Data Schemas in the context of Pandas?
* Luigi & why it is cool: https://www.slideshare.net/erikbern/luigi-presentation-nyc-data-science
* Good source: Luigi + Analytics + Validation + Warehouse https://github.com/groupon/luigi-warehouse

### Backend

### Frontend
* LINK: http://brianflove.com/2016/03/29/typescript-express-node-js/


## Considerations

* What is the anticipated scale? Which parts of the solution must scale?
* What kind of data anomalies exist? Duplicate IDs? Issues with missing IDs?

* Docker timeout / idle: https://github.com/godaddy/terminus