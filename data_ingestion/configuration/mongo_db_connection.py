import os
import sys

import certifi
import pymongo

from constant.data_ingestion import DATABASE_NAME, MONGODB_URL_KEY
from exception import TruckException

ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                
                if mongo_db_url is None:
                    raise Exception(f"Environment variable: {MONGODB_URL_KEY} is not set.")
                
                else:
                    if "localhost" in mongo_db_url:
                        MongoDBClient.client = pymongo.MongoClient(mongo_db_url)

                    else:
                        MongoDBClient.client = pymongo.MongoClient(
                            mongo_db_url, tlsCAFile=ca
                        )

            self.client = MongoDBClient.client

            self.database = self.client[database_name]

            self.database_name = database_name

        except Exception as e:
            raise TruckException(e, sys)
