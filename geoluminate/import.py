"""Utility functions for importing data into the geoluminate database."""

import pandas as pd

# define a one to one map of field names per model. The per measurement end user can override these mappings to
# customize the import process for their data.

PROJECT_FIELDS = {
    "title": "title",
}

DATASET_FIELDS = {
    "title": "title",
    "description": "description",
    "type": "type",
}

SAMPLE_FIELDS = {
    "title": "title",
    "description": "description",
    "type": "type",
}


class GeoluminateImporter:

    def __init__(self, file_obj):
        self.obj = file_obj
        self.df = pd.DataFrame(file_obj)

    def read_data(self):
        pass

    def import_data(self):
        project = self.save_project_data()
        dataset = self.save_dataset_data()
        sample = self.save_sample_data()
        measurement = self.save_measurement_data()

    def save_project_data(self, row):
        # go through PROJECT_FIELDS and extract mapped data from the dataframe row

        # create a model form field and attempt to save the data to the database

        # if it already exists, return the existing object

        # if it doesn't exist, create a new object and save it to the database, and return it
        pass

    def save_dataset_data(self, row):
        # go through DATASET_FIELDS and extract mapped data from the dataframe row

        # create a model form field and attempt to save the data to the database

        # if it already exists, return the existing object

        # if it doesn't exist, create a new object and save it to the database, and return it
        pass

    def save_sample_data(self, row):
        # go through SAMPLE_FIELDS and extract mapped data from the dataframe row

        # create a model form field and attempt to save the data to the database

        # if it already exists, return the existing object

        # if it doesn't exist, create a new object and save it to the database, and return it
        pass

    def save_measurement_data(self, row):
        # go through DATASET_FIELDS and extract mapped data from the dataframe row

        # create a model form field and attempt to save the data to the database

        # if it already exists, return the existing object

        # if it doesn't exist, create a new object and save it to the database, and return it
        pass
