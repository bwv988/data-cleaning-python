"""
pipeline.py - Data cleaning and ingestion pipeline with Luigi.
"""

import luigi

from luigi.mock import MockTarget 

class LoadData(luigi.Task):
    """
    This task loads the data.
    """
    def output(self):
        return MockTarget("LoadData", 
            mirror_on_stderr=True)
 
    def run(self):
        pass

class CleanData(luigi.Task):
    """
    This task defines business logic to clean the data.
    """
    def requires(self):
        return LoadData()

    def output(self):
        return MockTarget("CleanData", 
            mirror_on_stderr=True)
    
    def run(self):
        pass

class IngestData(luigi.Task):
    """
    Runs logic to ingest data into data warehouse.
    """
    def requires(self):
        return CleanData()

    def output(self):
        return MockTarget("IngestData", 
            mirror_on_stderr=True)
    
    def run(self):    
        pass
 
if __name__ == '__main__':
    luigi.run(["--local-scheduler"], 
        main_task_cls=IngestData)