from json import loads
from os import environ

from pandas import DataFrame
from pymongo import MongoClient

from utils.logger import AppLogger
from utils.main_utils import MainUtils
from utils.read_params import get_log_dic, read_params


class MongoDB_Operation:
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

        self.log_writer = AppLogger()

    def get_database(self, db_name, log_file):
        """
        Method Name :   get_database
        Description :   This method gets database from MongoDB from the db_name

        Output      :   A database is created in MongoDB with name as db_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_database.__name__, __file__, log_file
        )

        self.log_writer.info("start",)

        try:
            db = self.client[self.mongo_config[db_name]]

            self.log_writer.info(f"Created {db_name} database in MongoDB",)

            self.log_writer.info("exit",)

            return db

        except Exception as e:
            self.log_writer.info(e,)

    def get_collection_as_dataframe(self, db_name, collection_name, log_file):
        """
        Method Name :   get_collection_as_dataframe
        Description :   This method is used for converting the selected collection to dataframe

        Output      :   A collection is returned from the selected db_name and collection_name
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_collection_as_dataframe.__name__,
            __file__,
            log_file,
        )

        self.log_writer.info("start",)

        try:
            database = self.get_database(db_name,)

            collection_name = self.utils.get_collection_with_timestamp(collection_name,)

            collection = database.get_collection(collection_name)

            df = DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            self.log_writer.info("Converted collection to dataframe",)

            self.log_writer.info("exit",)

            return df

        except Exception as e:
            self.log_writer.info(e,)

    def insert_dataframe_as_record(
        self, data_frame, db_name, collection_name, log_file
    ):
        """
        Method Name :   insert_dataframe_as_record
        Description :   This method inserts the dataframe as record in database collection

        Output      :   The dataframe is inserted in database collection
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.insert_dataframe_as_record.__name__,
            __file__,
            log_file,
        )

        self.log_writer.info("start",)

        try:
            records = loads(data_frame.T.to_json()).values()

            self.log_writer.info(f"Converted dataframe to json records",)

            database = self.get_database(db_name,)

            collection_name = self.utils.get_collection_with_timestamp(collection_name,)

            collection = database.get_collection(collection_name)

            self.log_writer.info("Inserting records to MongoDB",)

            collection.insert_many(records)

            self.log_writer.info("Inserted records to MongoDB",)

            self.log_writer.info("exit",)

        except Exception as e:
            self.log_writer.info(e,)
