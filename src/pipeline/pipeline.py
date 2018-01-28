"""
warehouse.py - Ingest data into Data Warehouse.
"""

import luigi

from luigi.mock import MockTarget 

class LoadData(luigi.Task):
    def output(self):
        return MockTarget("LoadData", 
            mirror_on_stderr=True)
 
    def run(self):
        _write = self.output().open('w')
        _write.write(u"Loading of data completed.\n")
        _write.close()

class CleanData(luigi.Task): 
    def requires(self):
        return LoadData()

    def output(self):
        return MockTarget("CleanData", 
            mirror_on_stderr=True)
    
    def run(self):
        _read = self.input().open("r")
        _write = self.output().open('w')
        for first_ends in _read:
            outval = u"Second Task after "+first_ends+u"\n"
            _write.write(outval)
        
        _write.close()
        _read.close()

class IngestData(luigi.Task):
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