import json
from pymongo import MongoClient
from imports.base import dbBase
from imports.models import Base
import pandas as pd


# class ImportData(dbBase):
#     """ Inserts data into database ensuring there are not duplicates"""
#
#     def __init__(self, csv_file, db_location):
#         super().__init__(db_location)
#         self.db_location = db_location
#         self.csv_file = csv_file
#         Base.metadata.create_all(self.engine)
#         self.id_count = 1
#
#     def load_tables(self):
#         """load tables with data"""

class ImportData:
    def __init__(self, csv_path, db_name):
        self.csv_path = csv_path
        self.db_name = db_name
        self.collection_name = 'Covid_Data'
        self.db_url = '127.0.0.1'
        self.db_port = 27017

    def mongoimport(self):
        """ Imports a csv file at path csv_name to a mongo colection
        returns: count of the documants in the new collection
        """
        client = MongoClient(f"mongodb+srv://admin:Y775tR!fhwZ22my@cluster0.tfxlb.mongodb.net/{self.db_name}?retryWrites=true&w=majority")
        db = client.test
        #coll = db[self.collection_name]
        data = pd.read_csv(self.csv_path)
        #coll.insert_one(data.to_dict())
        return print(client.list_database_names())
