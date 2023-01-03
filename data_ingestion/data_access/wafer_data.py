import os
import sys
from typing import List

import pandas as pd
from pymongo.collection import Collection

from configuration.mongo_db_connection import MongoDBClient
from constant import DATABASE_NAME
from exception import WaferException
from logger import logging


class WaferData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise WaferException(e, sys)

    def export_collections_from_mongodb(self, data_dir: str):
        logging.info(
            "Entered export_collections_from_mongodb method of WaferData class"
        )

        try:
            os.makedirs(data_dir, exist_ok=True)

            collections: List[str] = self.mongo_client.database.list_collection_names()

            logging.info("Got a list of collection names from mongodb")

            for col in collections:
                db_col: Collection = self.mongo_client.database.get_collection(col)

                logging.info(f"Got a {db_col} collection from mongodb")

                df: pd.DataFrame = pd.DataFrame(list(db_col.find()))

                if "_id" in df.columns.to_list():
                    df: pd.DataFrame = df.drop(columns=["_id"], axis=1)

                logging.info(f"Created dataframe from {db_col} collection")

                fname: str = f"{data_dir}/{col}.csv"

                df.to_csv(fname, index=None, header=False)

                logging.info(f"Converted dataframe to {fname} csv file")

        except Exception as e:
            raise WaferException(e, sys)
