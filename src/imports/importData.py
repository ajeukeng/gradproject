import json
import urllib.parse

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
    def __init__(self, csv_path, db_name, db_pwd):
        self.csv_path = csv_path
        self.db_name = db_name
        self.collection_name = 'Covid_Data'
        self.client = None
        self.db_pwd = db_pwd

    def createDB(self):
        """ Creates database"""
        self.client = MongoClient(f"mongodb+srv://admin:{urllib.parse.quote(self.db_pwd)}@cluster0.tfxlb.mongodb.net/{self.db_name}?retryWrites=true&w=majority")
        return print(self.client.list_database_names())

    def addCollections(self):
        """Adds Collections to DB"""

        db = self.client.test
        db.collection.delete_many({})
        # data = pd.read_csv(self.csv_path)
        # db.collection.insert_many(data.to_dict('records'))
