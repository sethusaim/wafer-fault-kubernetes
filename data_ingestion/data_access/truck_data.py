import os
import sys
from typing import List

import pandas as pd
from pymongo.collection import Collection

from configuration.mongo_db_connection import MongoDBClient
from constant.data_ingestion import DATABASE_NAME
from exception import TruckException
from logger import logging

class TruckData:
    def __init__(self):
        """ """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise TruckException(e, sys)

    def export_collections_from_mongodb(self, data_dir: str):        
        try:
            os.makedirs(data_dir, exist_ok=True)

            collections: List[str] = self.mongo_client.database.list_collection_names()

            for col in collections:
                db_col: Collection = self.mongo_client.database.get_collection(col)

                df: pd.DataFrame = pd.DataFrame(list(db_col.find()))

                if "_id" in df.columns.to_list():
                    df: pd.DataFrame = df.drop(columns=["_id"], axis=1)

                fname: str = f"{data_dir}/{col}.csv"

                df.to_csv(fname, index=None, header=False)

        except Exception as e:
            raise TruckException(e, sys)
