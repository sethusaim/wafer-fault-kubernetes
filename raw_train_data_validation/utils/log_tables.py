from boto3 import client, resource

from utils.read_params import read_params


class Log_Table:
    def __init__(self):
        self.config = read_params()

        self.tables = list(self.config["log"].values())

        self.db_client = client("dynamodb")

        self.db_resource = resource("dynamodb")

        self.class_name = self.__class__.__name__

    def create_log_table(self, table_name):
        """
        Method Name :   create_log_table
        Description :   This method is used for creating the table for log

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.create_log_table.__name__

        try:
            response = self.db_client.list_tables()

            if table_name in response["TableNames"]:
                pass

            else:
                self.db_resource.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {"AttributeName": "Log_updated_date", "KeyType": "HASH"},
                    ],
                    AttributeDefinitions=[
                        {"AttributeName": "Log_updated_date", "AttributeType": "S"},
                    ],
                    ProvisionedThroughput={
                        "ReadCapacityUnits": 1000,
                        "WriteCapacityUnits": 1000,
                    },
                )

        except Exception as e:
            error_msg = f"Exception occured in Class : {self.class_name}, Method : {method_name}, Error : {str(e)}"

            raise Exception(error_msg)

    def generate_log_tables(self):
        """
        Method Name :   generate_table
        Description :   This method is used for creating the table for log

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.generate_log_tables.__name__

        try:
            [self.create_log_table(table) for table in self.tables]

        except Exception as e:
            error_msg = f"Exception occured in Class : {self.class_name}, Method : {method_name}, Error : {str(e)}"

            raise Exception(error_msg)
