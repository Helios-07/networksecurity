import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

import certifi
import pandas as pd
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            # Connect using certifi CA bundle
            mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

            # Access DB and collection
            db = mongo_client[database]
            col = db[collection]

            # Insert documents
            col.insert_many(records)

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"  # Ensure correct path separator
    DATABASE = "AMANAI"
    COLLECTION = "NetworkData"

    try:
        networkobj = NetworkDataExtract()
        records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
        print(f"Total records to insert: {len(records)}")
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"Inserted {no_of_records} records into MongoDB")
    except Exception as err:
        print(f"ERROR: {err}")
