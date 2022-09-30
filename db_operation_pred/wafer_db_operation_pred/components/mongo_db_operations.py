import logging
import sys
from json import loads
from os import environ

from pandas import DataFrame
from pymongo import MongoClient

from wafer_db_operation_pred.exception import WaferException
from wafer_db_operation_pred.utils.main_utils import MainUtils
from wafer_db_operation_pred.utils.read_params import read_params


class MongoDBOperation:
    """
    Description :   This method is used for all mongodb operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.config = read_params()

        self.DB_URL = environ["MONGODB_URL"]

        self.mongo_config = self.config["mongodb"]

        self.client = MongoClient(self.DB_URL)

        self.utils = MainUtils()

        self.log_writer = logging.getLogger(__name__)

    def get_database(self, db_name):
        """
        Method Name :   get_database
        Description :   This method gets database from MongoDB from the db_name

        Output      :   A database is created in MongoDB with name as db_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info("Entered get_database method of MongoDBOperation class")

        try:
            db = self.client[self.mongo_config[db_name]]

            self.log_writer.info(f"Created {db_name} database in MongoDB")

            self.log_writer.info("Exited get_database method of MongoDBOperation class")

            return db

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def get_collection_as_dataframe(self, db_name, collection_name):
        """
        Method Name :   get_collection_as_dataframe
        Description :   This method is used for converting the selected collection to dataframe

        Output      :   A collection is returned from the selected db_name and collection_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered get_collection_as_dataframe method of MongoDBOperation class"
        )

        try:
            database = self.get_database(db_name)

            collection_name = self.utils.get_collection_with_timestamp(collection_name,)

            collection = database.get_collection(collection_name)

            df = DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            self.log_writer.info("Converted collection to dataframe")

            self.log_writer.info(
                "Exited get_collection_as_dataframe method of MongoDBOperation class"
            )

            return df

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a

    def insert_dataframe_as_record(self, data_frame, db_name, collection_name):
        """
        Method Name :   insert_dataframe_as_record
        Description :   This method inserts the dataframe as record in database collection

        Output      :   The dataframe is inserted in database collection
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        self.log_writer.info(
            "Entered insert_dataframe_as_record method of MongoDBOperation class"
        )

        try:
            records = loads(data_frame.T.to_json()).values()

            self.log_writer.info(f"Converted dataframe to json records",)

            database = self.get_database(db_name)

            collection_name = self.utils.get_collection_with_timestamp(collection_name,)

            collection = database.get_collection(collection_name)

            self.log_writer.info("Inserting records to MongoDB",)

            collection.insert_many(records)

            self.log_writer.info("Inserted records to MongoDB",)

            self.log_writer.info(
                "Exited insert_dataframe_as_record method of MongoDBOperation class"
            )

        except Exception as e:
<<<<<<< HEAD
            

            

            
=======
            raise WaferException(e, sys) from e
>>>>>>> 9a49ca66aedf49b9aa306b47001004e3aaa9192a
