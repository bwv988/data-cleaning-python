"""
data_cleaner.py - Data cleaning and validation module.

This should be invoked as a Luigi task.
"""

from lib import airlines, airports, routes

class DataCleaner():
    """
    A factory class that calls concrete implementations for validating 
    and cleaning different rows in different data sets.

    The idea is that each domain object has different validation and cleaning needs.
    But we want to use a generic API to invoke these.
    """

    def __init__(self, factory):
        self.factory = factory

    def validate(self):
        """ 
        Validate the data frame.

        FIXME: Not doing anything here. Should be implemented. Also: Add assertions etc.
        FIXME: Ideally, this should be based on pre-defined data schemas.
        FIXME: Do more research on data schema validation in the context of Pandas data frames.
        """

        self.factory.validate()
    
    def clean(self):
        """
        Invoke cleaning strategy for the respective data.
        """
        
        self.factory.clean()


def main():
    """
    Entry point.
    """

    df = None
    airports_cl = DataCleaner(airports.Airports(df))
    airlines_cl = DataCleaner(airlines.Airlines(df))
    routes_cl = DataCleaner(routes.Routes(df))

    print("Validating all data data...")
    airports_cl.validate()
    airlines_cl.validate()
    routes_cl.validate()

    print("Cleaning all data data...")

    airports_cl.clean()
    airlines_cl.clean()
    routes_cl.clean()
    

if __name__ == "__main__": 
    main()